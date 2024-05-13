import requests
import json
from datetime import datetime, timezone

expiration_file = '/home/snparada/Spacionatural/Libraries/laudus_lib/creds/expirationDate.json'
token_file = '/home/snparada/Spacionatural/Libraries/laudus_lib/creds/laudusToken.json'

# Leer la fecha de expiración desde el archivo
try:
    with open(expiration_file, 'r') as f:
        expiration_date_str = json.load(f)['expiration']
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%dT%H:%M:%S%z')
except (FileNotFoundError, KeyError):
    expiration_date = datetime.now(timezone.utc)

# Si el token está expirado, obtener uno nuevo
if datetime.now(timezone.utc) >= expiration_date:
    url = "https://api.laudus.cl/security/login"

    body = {
        "userName": "api",
        "password": "laudus",
        "companyVATId": "76015239-0"
    }

    response = requests.post(url, json=body)

    if response.status_code == 200:
        data = response.json()
        token = data['token']
        expiration_date_str = data['expiration']
        
        # Guardar el token y la fecha de expiración en los archivos
        with open(token_file, 'w') as f:
            json.dump({'token': token}, f)
            
        with open(expiration_file, 'w') as f:
            json.dump({'expiration': expiration_date_str}, f)
            
else:
    # Si el token no está expirado, leerlo desde el archivo
    with open(token_file, 'r') as f:
        token = json.load(f)['token']
