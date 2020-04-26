import asyncio
from pyppeteer import launch

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


async def probando(datos_ptp, lado):
    browser = await launch(headless=False)
    count = 0
    index = ['1', '2', '7', '22']
    fotos_nombre = ['\HOME', '\RADIO', '\ETHERNET', '\LINK STATUS']
    while count <= 3:
        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})
        final = str(datos_ptp['ip'] + '?mac_esn=' + datos_ptp['mac_esn'] + '&catindex=' + str(count) + '&pageindex=' + index[count] + '&Session=' + datos_ptp['Session'])
        await page.goto(final)
        print("abierto 1")
        await page.screenshot({'path': 'C:\guardadas' + fotos_nombre[count] + ' ' + lado + '.png', 'fullPage': True})
        count += 1
    await browser.close()

if __name__ == '__main__':
    url_lado_a = input("URL : ")
    lado = input("QUE LADO ES?: ")
    var_lado_a = parser_web(url_lado_a)
    asyncio.get_event_loop().run_until_complete(probando(var_lado_a, lado))


