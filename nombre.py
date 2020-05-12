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
#from pyppeteer import errors


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
    #listas['PATH'] = full_path2
    if c_mon2 == '2':
        window_pos = '--window-position=' + listas['WIDTH'] + ',0'
        print(window_pos)
    else:
        window_pos = '--window-position=0,0'
    window_size = '--window-size=' + listas['WIDTH']+','+ listas['HEIGHT']
    #args = ['--start-maximized', '--window-position=0,0', '--window-size=1440,900']
    args = ['--start-maximized', window_pos, window_size]
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
        print("abierto 1")
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
    await browser.close()

def parse_web_pmp(url):
    #full_url = 'http://10.25.78.200/#home' or similar
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
    if c_mon2 == '2':
        window_pos = '--window-position=' + listas['WIDTH'] + ',0'
        print(window_pos)
    else:
        window_pos = '--window-position=0,0'
    window_size = '--window-size=' + listas['WIDTH']+','+ listas['HEIGHT']
    args = ['--start-maximized', window_pos, window_size]

    browser = await launch(headless=False, defaultViewport=None, args=args)
    cont2 = 0
    paginas = ['#home', '#config:network_config', '#config:radio', '#config:system', '#config:quality_of_service']
    nombres = ['HOME', 'NETWORK', 'RADIO', 'SYSTEM', 'QOS']
    ip = parse_object.netloc
    octetos = ip.split(".")
    try:
        if octetos[1] == "15":
            print("Huancavelica")
        elif octetos[1] == "25":
            print("Ayacucho")
        elif octetos[1] == "35":
            print("Apurimac")
        elif octetos[1] == "45":
            print("cusco")
        else:
            print("No es un octeto valido")
    except IndexError:
        messagebox.showerror(title="Problemas de Url", message="Url mal ingresada")
        await browser.close()
    while cont2 <= 4:
        page = await browser.newPage()
        await page.setViewport({'width': int(listas['WIDTH']), 'height': int(listas['HEIGHT'])})
        if is_pmp is False and cont2 == 4:
            break
        url_final = str(parse_object.scheme + '://' + parse_object.netloc + parse_object.path + paginas[cont2])
        print(url_final)
        try:
            await page.goto(url_final, {'waitUntil': 'load', 'timeout': 15000})
        except:
            await browser.close()
        print("Página abierta")

        if octetos[1] == "45" and cont2 == 0:
            await page.waitFor(3000)
            await page.type("input[name=username", text="admin")
            await page.type("input[name=password]", text="admin")
            await page.click("#loginBtn")

        if octetos[1] != "45" and cont2 == 0:
            await page.type("input[name=username", text="admin")
            await page.type("input[name=password]", text="$Sat4528Reg$")
            await page.click("#loginBtn")
            print("funciona?")

        captura_pantallas = mss(display=':0.0')
        nombre_archivo = nombres[cont2] + '.png'
        print("Nombre archivo: " + nombre_archivo)
        print("Este es el c_dir2: " + c_dir2)
        path_finall = os.path.join(c_dir2, nombre_archivo)
        print("Ruta final a guardar cada archivo: " + path_finall)
        await page.waitForSelector("#main_content", {'visible': True})
        ###################### MODIFICADO
        #await page.waitFor(800)
        print("imprimes?")
        captura_pantallas.shot(mon=int(listas['MON']), output=path_finall)
        print("impreso")
        ###############################MODO
        if is_pmp is True and cont2==4 and octetos[1] != "45":
            await page.click("a#login_dropdown")
            await page.click("#loginBtn")
        elif is_pmp is False and cont2 == 3 and octetos[1] != "45":
            await page.click("a#login_dropdown")
            await page.click("#loginBtn")
        elif is_pmp is True and cont2 == 4 and octetos[1] == "45":
            print("Clickea antes")
            await page.click("a#login_dropdown")
            await page.click("#loginBtn")
            print("Clickea despues")
        elif is_pmp is False and cont2 == 3 and octetos[1] == "45":
            await page.click("a#login_dropdown")
            await page.click("#loginBtn")
        print(str(cont2) + " antes de hacer el ciclo")
        cont2+= 1

    time.sleep(3)
    await browser.close()

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
    # else:
    #     messagebox.showinfo(title="Ups!", messagebox="Escoje un tipo de enlace!")
    #     print("Escoje un tipo de enlace")

    print("Se ha seleccionado la opcion " + str(selected.get()))
    print(url_input.get())


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
    print(script_dir)
    print(full_path)
    f = open(full_path, "w")
    config.write(f)
    f.close()


window = Tk()
window.title("En progreso...")
window.geometry()

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Principal')
tab_control.add(tab2, text='Configuracion')
tab_control.pack(expand=1, fill='both')

selected = IntVar()
rad1 = Radiobutton(tab1, text='PTP', value=1, variable=selected, font=("Arial", 13))
rad2 = Radiobutton(tab1, text='PMP', value=2, variable=selected, font=("Arial", 13))
rad3 = Radiobutton(tab1, text='CPE', value=3, variable=selected, font=("Arial", 13))
rad1.grid(column=0, row=4)
rad2.grid(column=1, row=4)
rad3.grid(column=2, row=4)

url_label = Label(tab1, text="URL: ", font=("Arial"))
url_label.grid(row=0, sticky=W)
url_input = Entry(tab1, width=30)
url_input.grid(row=0, column=1)

side_label = Label(tab1, text="Lado: ", font=("Arial"))
side_label.grid(row=1, sticky=W)
side_input = Entry(tab1, width=30)
side_input.grid(row=1, column=1)

btn = Button(tab1, text='CAPTURA', bg='black', fg='white', command=clicked)
btn.grid(column=0, row=3, columnspan=3)

#################### PANTALLA DE CONFIGURACION ###############################
dimension_label = Label(tab2, text="Dimensiones: ", font=("Arial"))
dimension_label.grid(row=0, column=0, sticky=W)
width_input = Entry(tab2, width=5)
width_input.grid(row=0, column=1)
width_input.insert(0, c_width)
producto_label = Label(tab2, text="X")
producto_label.grid(row=0, column=2)
height_input = Entry(tab2, width=5)
height_input.grid(row=0, column=3)
height_input.insert(0, c_height)

directorio = Button(tab2, text="Directorio", command=abrir_archivo)
directorio.grid(row=1, column=0)

directry_label = Label(tab2, text=c_dir)
directry_label.grid(column=1, row=1, columnspan=3, sticky=W)

monitor_titulo = Label(tab2, text="Monitor a usar: ", font=("Arial", 15))
monitor_titulo.grid(column=0, row=2, columnspan=4)
selected2 = IntVar()
mon_izq = Radiobutton(tab2, text='Izquierdo', value=1, variable=selected2, font=("Arial"))
mon_der = Radiobutton(tab2, text='Derecho', value=2, variable=selected2, font=("Arial"))
selected2.set(int(c_mon))
mon_izq.grid(column=0, row=3)
mon_der.grid(column=1, row=3)
btn_guardar = Button(tab2, text='GUARDAR', bg='black', fg='white', command=guardar_cambios)
btn_guardar.grid(column=0, row=4, columnspan=3)


if __name__ == '__main__':
    window.mainloop()




