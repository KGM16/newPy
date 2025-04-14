#En base al .har que te cargue, quiero que el . py tome los correos de un un txt que se llama correos.txt
#y pues remplazas kendall.gomez por le correo que este en la lista de correos y que envie cada correo de 1 por 20 segundos. esto para que no 
#me de un time out la pagina. 


import time
import requests
import os

def enviar_correo(correo):
    url = "https://softland.zendesk.com/access/help"
    data = {
        "authenticity_token": "0PpezpUpE3fWxK4hOc2dpNGgrGVknUCSalGwpRTQBE",
        "return_to_on_failure": "https://softland.zendesk.com/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&return_to=https%3A%2F%2Fsoftland.zendesk.com%2Fhc%2Fes%2Frequests%3Fquery%3D%26page%3D1%26selected_tab_name%3Dmy-requests&theme=hc",
        "return_to": "https://softland.zendesk.com/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&return_to=https%3A%2F%2Fsoftland.zendesk.com%2Fhc%2Fes%2Frequests%3Fquery%3D%26page%3D1%26selected_tab_name%3Dmy-requests&theme=hc",
        "email": correo,
        "brand_id": "360000349757",
        "auth_origin": "360000349757%2Cfalse%2Ctrue",
        "theme": "hc",
        "role": "",
        "commit": "Enviar"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
    }

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print(f"Correo enviado a {correo}")
    else:
        print(f"Error al enviar correo a {correo}: {response.status_code}")

def main():
    ruta_archivo = 'C:/Users/kgomezm/Desktop/temp/logs/correos.txt'
    ruta_existen = 'C:/Users/kgomezm/Desktop/temp/logs/existen.txt'
    ruta_no_existen = 'C:/Users/kgomezm/Desktop/temp/logs/no-existen.txt'

    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return

    with open(ruta_archivo, 'r') as file:
        correos = file.readlines()

    correos_existentes = []
    correos_no_existentes = []

    for correo in correos:
        correo = correo.strip()  # Eliminar espacios en blanco y saltos de línea
        try:
            enviar_correo(correo)
            correos_existentes.append(correo)
        except requests.exceptions.RequestException as e:
            print(f"Error al enviar correo a {correo}: {e}")
            correos_no_existentes.append(correo)
        time.sleep(20)  # Esperar 20 segundos antes de procesar el siguiente correo

    # Guardar correos existentes en un archivo
    with open(ruta_existen, 'w') as file:
        for correo in correos_existentes:
            file.write(correo + '\n')

    # Guardar correos no existentes en un archivo
    with open(ruta_no_existen, 'w') as file:
        for correo in correos_no_existentes:
            file.write(correo + '\n')

    print("Correos existentes guardados en:", ruta_existen)
    print("Correos no existentes guardados en:", ruta_no_existen)

if __name__ == "__main__":
    main()
