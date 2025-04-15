import requests
from bs4 import BeautifulSoup

# Inicializa una sesión para mantener las cookies
session = requests.Session()

# URL del formulario donde se encuentra el token válido
form_url = "https://softland.zendesk.com/auth/v2/login/password_reset"

# Realiza una solicitud GET para obtener la página del formulario
get_response = session.get(form_url)
if get_response.status_code != 200:
    print("Error al obtener el formulario:", get_response.status_code)
    exit()

# Utiliza BeautifulSoup para parsear el HTML y extraer el token
soup = BeautifulSoup(get_response.text, 'html.parser')
token_input = soup.find("input", {"name": "authenticity_token"})

if token_input and token_input.get("value"):
    authenticity_token = token_input.get("value")
    print("Token obtenido:", authenticity_token)
else:
    print("No se pudo encontrar el token de autenticidad en la página.")
    exit()

# Prepara la URL y el payload para la solicitud POST
post_url = "https://softland.zendesk.com/access/help"

# Los valores de los campos deben ser acordes a lo que el formulario espera.
# Nota: Asegúrate de que los parámetros return_to, return_to_on_failure y auth_origin
# sean los correctos para tu entorno. Aquí se usan ejemplos basados en lo que se ha mostrado.
payload = {
    "authenticity_token": authenticity_token,
    "return_to_on_failure": "/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&role=&theme=hc",
    "return_to": "https://softland.zendesk.com/auth/v2/login/password_reset?auth_origin=360000349757%2Cfalse%2Ctrue&brand_id=360000349757&theme=hc",
    "email": "daniel.torres@farmagro.co.cr",
    "brand_id": "360000349757",
    "auth_origin": "360000349757%2Cfalse%2Ctrue",  # Código URL encoded (o su equivalente sin codificar, según la API)
    "theme": "hc",
    "role": "",
    "commit": "Enviar"
}

# Establece el header adecuado para formularios URL encoded
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Realiza la solicitud POST usando la misma sesión (para preservar cookies)
post_response = session.post(post_url, data=payload, headers=headers)

# Imprime el estado y respuesta del POST para verificar el resultado
print("Código de estado de la respuesta POST:", post_response.status_code)
print("Respuesta del servidor:")
print(post_response.text)
