import asyncio
from pyppeteer import launch
from mss import mss
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import configparser
import time
from urllib.parse import urlparse


def parser_web(url):
    rutas = url.split('?')
    ruta_principal = rutas[0]
    anexos = rutas[1].split('&')
    print(anexos)
    datos_ptp = {}
    for valores in anexos:
        valor = valores.split('=')
        datos_ptp[valor[0]] = valor[1]
    datos_ptp['ip'] = ruta_principal
    return datos_ptp


async def PTP(datos_ptp, lado):
    c_width2 = config['DIMENSION']['width']
    c_height2 = config['DIMENSION']['height']
    c_dir2 = config['RUTA']['dir']
    c_mon2 = config['MONITOR']['mon']
    listas = {}
    listas['WIDTH'] = c_width2
    listas['HEIGHT'] = c_height2
    listas['DIR'] = c_dir2
    listas['MON'] = c_mon2
    if c_mon2 == '2':
        window_pos = '--window-position=' + listas['WIDTH'] + ',0'
        print(window_pos)
    else:
        window_pos = '--window-position=0,0'
    window_size = '--window-size=' + listas['WIDTH']+','+ listas['HEIGHT']
    args = ['--start-maximized', window_pos, window_size, '--ignore-certificate-errors', '--disable-infobars']
    print(args)
    browser = await launch(headless=False, defaultViewport=None, args=args)
    count = 0
    index = ['1', '2', '7', '22']
    fotos_nombre = ['HOME', 'RADIO', 'ETHERNET', 'LINK STATUS']
    while count <= 3:
        page = await browser.newPage()
        await page.setViewport({'width': int(listas['WIDTH']), 'height': int(listas['HEIGHT'])})
        final = str(datos_ptp['ip'] + '?mac_esn=' + datos_ptp['mac_esn'] + '&catindex=' + str(count) + '&pageindex=' + index[count] + '&Session=' + datos_ptp['Session'])
        await page.goto(final, {'waitUntil': 'load'})
        if count == 1:
            for i in range(0, 10):
                await page.keyboard.press("ArrowDown")
            await page.waitFor(500)
        if count == 3:
            for i in range(0, 10):
            #     await page.keyboard.press("ArrowDown")
                await page.keyboard.press("PageDown")
            await page.waitFor(600)
        print("abierto " + str(count))
        captura_pantallas = mss(display=':0.0')
        nombre_archivo = fotos_nombre[count] + ' ' + lado + '.png'
        print("Nombre archivo: " + nombre_archivo)
        print("Este es el c_dir2: " + c_dir2)
        path_finall = os.path.join(c_dir2, nombre_archivo)
        print("Ruta final a guardar cada archivo: " + path_finall)
        time.sleep(.500)
        captura_pantallas.shot(mon=int(listas['MON']), output=path_finall)
        print("impreso")
        count += 1
    await asyncio.sleep(1)
    await browser.close()

def parse_web_pmp(url):
    parse_object = urlparse(url)
    fragmento = parse_object.fragment
    ip = parse_object.netloc
    print(ip)
    print(fragmento)
    return parse_object


async def pmp(parse_object, is_pmp):
    c_width2 = config['DIMENSION']['width']
    c_height2 = config['DIMENSION']['height']
    c_dir2 = config['RUTA']['dir']
    c_mon2 = config['MONITOR']['mon']
    listas = {}
    listas['WIDTH'] = c_width2
    listas['HEIGHT'] = c_height2
    listas['DIR'] = c_dir2
    listas['MON'] = c_mon2
    ip2 = parse_object.netloc
    octetos2 = ip2.split(".")
    if octetos2[1] == "15":
        print("Huancavelica")
    elif octetos2[1] == "25":
        print("Ayacucho")
    elif octetos2[1] == "35":
        print("Apurimac")
    elif octetos2[1] == "45":
        print("cusco")
    else:
        exit(1)

    if c_mon2 == '2':
        window_pos = '--window-position=' + listas['WIDTH'] + ',0'
        print(window_pos)
    else:
        window_pos = '--window-position=0,0'
    window_size = '--window-size=' + listas['WIDTH']+','+ listas['HEIGHT']
    args = ['--start-maximized', window_pos, window_size, '--ignore-certificate-errors']

    browser = await launch(headless=False, defaultViewport=None, args=args)
    ip = parse_object.netloc
    octetos = ip.split(".")
    page = await browser.newPage()
    await page.setViewport({'width': int(listas['WIDTH']), 'height': int(listas['HEIGHT'])})

    url_final = str(parse_object.scheme + '://' + parse_object.netloc + parse_object.path + "#home")
    print(url_final)
    try:
        await page.goto(url_final, {'waitUntil': 'load', 'timeout': 15000})
    except:
        print("Página cerrada despues de 15 cargandola")
        await browser.close()
    print("Página abierta")

    if octetos[1] == "45":
        await page.waitFor(1000)
        await page.type("input[name=username", text="admin")
        await page.type("input[name=password]", text="admin")
        await page.click("#loginBtn")

    if octetos[1] != "45":
        await page.type("input[name=username", text="admin")
        await page.type("input[name=password]", text="$Sat4528Reg$")
        await page.click("#loginBtn")

    captura_pantallas = mss(display=':0.0')
    await page.waitForSelector("#main_content", {'visible': True})#HOME
    path_home = os.path.join(c_dir2, "HOME.png")
    await asyncio.sleep(0.4)
    captura_pantallas.shot(mon=int(listas['MON']), output=path_home)
    await page.click("#config\:radio_side_rootmenuitem")
    await asyncio.sleep(0.4)

    path_radio = os.path.join(c_dir2, "RADIO.png")
    await page.click("#config\:radio_side_menuitem") #RADIO
    await page.waitForSelector("#radio > h3", {'visible': True})
    await asyncio.sleep(0.4)
    captura_pantallas.shot(mon=int(listas['MON']), output=path_radio)
    await asyncio.sleep(0.4)

    path_system = os.path.join(c_dir2, "SYSTEM.png") #SYSTEM
    await page.click("#config\:system_side_menuitem")
    await page.waitForSelector("#system > h3", {'visible': True})
    await asyncio.sleep(0.4)
    captura_pantallas.shot(mon=int(listas['MON']), output=path_system)
    await asyncio.sleep(0.4)

    path_network = os.path.join(c_dir2, "NETWORK.png") #NETWORK
    await page.click("#config\:network_config_side_menuitem")
    await page.waitForSelector("#network_config > h3", {'visible': True})
    await asyncio.sleep(0.4)
    captura_pantallas.shot(mon=int(listas['MON']), output=path_network)
    await asyncio.sleep(0.4)

    if is_pmp is True:
        path_qos = os.path.join(c_dir2, "QOS.png") #QUALITY_OF_SERVICE
        await page.click("#config\:quality_of_service_side_menuitem")
        await page.waitForSelector("#quality_of_service > h3", {'visible': True})
        await asyncio.sleep(0.4)
        captura_pantallas.shot(mon=int(listas['MON']), output=path_qos)
        await asyncio.sleep(0.4)

    await page.click("a#login_dropdown")
    await page.click("#loginBtn")
    await asyncio.sleep(1)
    await browser.close()
    print("Navegador Cerrado")



config = configparser.ConfigParser()
config.read('dos.ini')
c_width = config['DIMENSION']['width']
c_height = config['DIMENSION']['height']
c_dir = config['RUTA']['dir']
c_mon = config['MONITOR']['mon']
script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path = "dos.ini"
full_path = os.path.join(script_dir, rel_path)


def clicked():

    if selected.get() == 1:
        try:
            url_lado_a = parser_web(url_input.get())
            print("PTP")
            asyncio.get_event_loop().run_until_complete(PTP(url_lado_a, side_input.get()))
            window.iconify()
        except:
            messagebox.showinfo(title="Ups!", message="revisa la url PTP nuevamente")
            print("Vuelve a escribir")
    elif selected.get() == 2:
        try:
            url_lado = parse_web_pmp(url_input.get())
            asyncio.get_event_loop().run_until_complete(pmp(url_lado, True))
            print("PMP")
            window.iconify()
        except:
            messagebox.showinfo(title="Ups!", message="revisa la url PMP nuevamente")
    elif selected.get() == 0:
        messagebox.showinfo(title="Ups!",message="Selecciona un enlace a capturar")
    elif selected.get() == 3:
        try:
            url_lado = parse_web_pmp(url_input.get())
            asyncio.get_event_loop().run_until_complete(pmp(url_lado, False))
            print("CPE")
            window.iconify()
        except:
            messagebox.showinfo(title="Ups!", message="revisa la url CPE nuevamente")


    print("Se ha seleccionado la opcion " + str(selected.get()))
    print(url_input.get())
    print("######### CAPTURADORA LISTA ###############")


def abrir_archivo():
    c2_dir = config['RUTA']['dir']
    directory = filedialog.askdirectory(initialdir=c2_dir)
    if directory !="":
        os.chdir(directory)
        directry_label.configure(text=os.getcwd())

    print(os.getcwd())
def guardar_cambios():
    config.set('RUTA', 'dir', os.getcwd())
    config.set('DIMENSION', 'width', width_input.get())
    config.set('DIMENSION', 'height', height_input.get())
    config.set('MONITOR', 'mon', str(selected2.get()))
    #print(script_dir)
    #print(full_path)
    f = open(full_path, "w")
    config.write(f)
    f.close()
    print("Cambios Guardados!")


window = Tk()
window.title("Capture Comm")
window.geometry()

tab_control = ttk.Notebook(window)
style = ttk.Style()
style.configure("BW.TLabel", background="#d6dbec")
tab1 = ttk.Frame(tab_control, style="BW.TLabel")
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Principal')
tab_control.add(tab2, text='Configuracion')
tab_control.pack(expand=1, fill='both')

selected = IntVar()
rad1 = Radiobutton(tab1, text='PTP', value=1, variable=selected, font=("Arial", 13))
rad2 = Radiobutton(tab1, text='PMP', value=2, variable=selected, font=("Arial", 13))
rad3 = Radiobutton(tab1, text='CPE', value=3, variable=selected, font=("Arial", 13))
rad1.grid(column=0, row=4, pady=8)
rad2.grid(column=1, row=4)
rad3.grid(column=2, row=4)

url_label = Label(tab1, text="Url: ", font=("Arial"))
url_label.grid(row=0, sticky=W, padx=10, pady=2)
url_input = Entry(tab1, width=30)
url_input.grid(row=0, column=1, ipadx=2, ipady=2)

side_label = Label(tab1, text="Lado: ", font=("Arial"))
side_label.grid(row=1, sticky=W, padx=10, pady=2)
side_input = Entry(tab1, width=30)
side_input.grid(row=1, column=1, ipadx=2, ipady=2)

btn = Button(tab1, text='CAPTURA', bg='black', fg='white', command=clicked, bd=3)
btn.grid(column=0, row=3, columnspan=3, pady=3)

#################### PANTALLA DE CONFIGURACION ###############################
dimension_label = Label(tab2, text="Dimensiones: ", font=("Arial"))
dimension_label.grid(row=0, column=0, sticky=W, pady=5)
width_input = Entry(tab2, width=5)
width_input.grid(row=0, column=1, ipadx=2, ipady=2)
width_input.insert(0, c_width)
producto_label = Label(tab2, text="X")
producto_label.grid(row=0, column=2)
height_input = Entry(tab2, width=5)
height_input.grid(row=0, column=3, ipadx=2, ipady=2)
height_input.insert(0, c_height)

directorio = Button(tab2, text="Guardar en: ", command=abrir_archivo, bg='#834639', fg='white')
directorio.grid(row=1, column=0)

directry_label = Label(tab2, text=c_dir)
directry_label.grid(column=1, row=1, columnspan=3, sticky=W)

monitor_titulo = Label(tab2, text="Monitor a usar: ", font=("Arial"))
monitor_titulo.grid(column=0, row=2, pady=3)
selected2 = IntVar()
mon_izq = Radiobutton(tab2, text='Izquierdo', value=1, variable=selected2, font=("Arial", 11))
mon_der = Radiobutton(tab2, text='Derecho', value=2, variable=selected2, font=("Arial", 11))
selected2.set(int(c_mon))
mon_izq.grid(column=0, row=3)
mon_der.grid(column=1, row=3)
btn_guardar = Button(tab2, text='GUARDAR', bg='black', fg='white', command=guardar_cambios)
btn_guardar.grid(column=0, row=4, columnspan=3, pady=5)


if __name__ == '__main__':
    window.mainloop()
