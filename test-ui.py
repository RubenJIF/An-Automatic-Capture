import asyncio
import pyautogui
from pyppeteer import launch
from mss import mss
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import configparser


async def main():
    # config2 = configparser.ConfigParser()
    # config2.read('dos.ini')
    c_width2 = config['DIMENSION']['width']
    c_height2 = config['DIMENSION']['height']
    c_dir2 = config['RUTA']['dir']
    c_mon2 = config['MONITOR']['mon']
    # script_dir2 = os.path.dirname(__file__)
    # rel_path2 = "dos.ini"
    path_nombre= "rubencito.png"
    full_path2 = os.path.join(c_dir2, path_nombre)
    listas = {}
    listas['WIDTH'] = c_width2
    listas['HEIGHT'] = c_height2
    listas['DIR'] = c_dir2
    listas['MON'] = c_mon2
    listas['PATH'] = full_path2

    args = ['--start-maximized', '--window-position=0,0', '--window-size=1440,900']
    browser = await launch(headless=False, defaultViewport=None, args=args)
    page = await browser.newPage()
    await page.setViewport({'width': int(listas['WIDTH']), 'height': int(listas['HEIGHT'])})
    await page.goto(url_input.get(), {'waitUntil': 'load'})
    print("abierto 1")
    captura_pantallas = mss(display=':0.0')
    captura_pantallas.shot(mon=int(listas['MON']), output=listas['PATH'])
    print("hecho")
    #myScreenshot = pyautogui.screenshot(region=(0,0,1221,448))
    #myScreenshot.save(r'C:\guardadas\sruben.png')
    # await page.screenshot({'path': 'C:\guardadas\screen1.png', 'fullPage': True})
    await browser.close()

config = configparser.ConfigParser()
config.read('dos.ini')
c_width = config['DIMENSION']['width']
c_height = config['DIMENSION']['height']
c_dir = config['RUTA']['dir']
c_mon = config['MONITOR']['mon']
script_dir = os.path.dirname(__file__)
rel_path = "dos.ini"
full_path = os.path.join(script_dir, rel_path)


def clicked():
    print(selected.get())
    print(url_input.get())
    asyncio.get_event_loop().run_until_complete(main())
    window.iconify()

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

window.mainloop()
