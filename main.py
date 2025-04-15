import time
import requests
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template_string, jsonify
import threading

app = Flask(__name__)

FORM_URL = "https://softland.zendesk.com/auth/v2/login/password_reset"
POST_URL = "https://softland.zendesk.com/access/help"

FIXED_PAYLOAD = {
    "return_to_on_failure": "/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&role=&theme=hc",
    "return_to": "https://softland.zendesk.com/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&theme=hc",
    "brand_id": "360000349757",
    "auth_origin": "360000349757%2Cfalse%2Ctrue",
    "theme": "hc",
    "role": "",
    "commit": "Enviar"
}

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}

def obtener_token(session):
    try:
        response = session.get(FORM_URL)
        response.raise_for_status()
    except Exception as e:
        print("Error al obtener el formulario:", e)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find("input", {"name": "authenticity_token"})
    return token_input.get("value") if token_input and token_input.get("value") else None

def procesar_correo(correo):
    session = requests.Session()
    token = obtener_token(session)
    if not token:
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"Fallo al obtener token para el correo {correo}\n")
        return

    payload = {
        "authenticity_token": token,
        "email": correo
    }
    payload.update(FIXED_PAYLOAD)

    try:
        post_response = session.post(POST_URL, data=payload, headers=HEADERS)
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"se procesó el correo {correo} - Código {post_response.status_code}\n")
        print(f"Correo {correo}: procesado - Código {post_response.status_code}")
    except Exception as e:
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"Error procesando {correo}: {e}\n")
        print(f"Error procesando {correo}: {e}")

@app.route("/")
def mostrar_log():
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        contenido = "log.txt no encontrado."
    return render_template_string("""
    <html>
    <head>
        <title>Log Viewer</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h2>Contenido de log.txt</h2>
        <pre style="background-color:#eee; padding:1em;">{{ contenido }}</pre>
    </body>
    </html>
    """, contenido=contenido)

def ejecutar_proceso():
    input_path = "correos.txt"

    if not os.path.exists(input_path):
        print(f"Archivo {input_path} no encontrado.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        correos = [line.strip() for line in f if line.strip()]

    for correo in correos:
        procesar_correo(correo)
        time.sleep(2)

if __name__ == "__main__":
    # Ejecutar el proceso de correos en un hilo separado
    proceso_thread = threading.Thread(target=ejecutar_proceso)
    proceso_thread.start()
    # Iniciar el servidor Flask
    app.run(host="0.0.0.0", port=8080)
