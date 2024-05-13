import json
import requests



def getToken():
    # Abre el archivo y lee su contenido
    with open('/home/sam/Spacionatural/creds/laudusToken.json', 'r') as file:
        data = json.load(file)

    # Obtén el valor de la clave 'token'
    token_value = data['token']
    return token_value

def headers_authorization(token):

    auth_token = 'Bearer '+token
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': auth_token
    }

    return headers

def get_data(url,headers_auth,parametros={}):
    response = requests.get(url, headers=headers_auth, json=parametros)
    result = {'status': False, 'response': None}
    if response.status_code == 200:
        result['status'] = True

        result['response'] = response.json()
    elif response.status_code == 204:
        result['status'] = False
    else:
        print(
            f'Error en la busqueda de la url: {url}, respuesta del servidor: {response.text}')
    return result

def get_stock(url):
    tokenLaudus = getToken()
    # print(tokenLaudus)

    headers_auth = headers_authorization(tokenLaudus)
    # print(headers_auth)
    jsonStock = get_data(url,headers_auth)    
    
    return jsonStock






