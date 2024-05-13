import requests
import xml.etree.ElementTree as ET
from Sincronizacion_Stock.api.urls import JSON_COMBINATIONS_BY_REFERENCE, JSON_PRODUCTS_BY_REFERENCE
from Sincronizacion_Stock.api.key.prestashopKey import PRESTASHOP_KEY
from lxml import etree

headers_json = {'Content-Type': 'application/json'}

HEADERS_XML = {
    'Content-Type': 'application/xml',  # especifica que enviarás XML
    # especifica que aceptarás XML como respuesta (opcional)
    'Accept': 'application/xml'
}


def get_data_json(url):
    response = requests.get(url, auth=(
        PRESTASHOP_KEY, ''), headers=headers_json)
    result = {'status': False, 'response': None}
    if response.status_code == 200:
        result['status'] = True
        result['response'] = response.json()
    else:
        print(
            f'Error en la busqueda de la url: {url}, respuesta del servidor: {response.text}')
    return result


def get_data_xml(url):
    response = requests.get(url, auth=(
        PRESTASHOP_KEY, ''), headers=HEADERS_XML)
    result = {'status': False, 'response': None}
    if response.status_code == 200:
        result['status'] = True
        # print(f'este es xml {response.text}')
        result['response'] = response.text
        # print (f'este es el result {result["response"]}')
    else:
        print(
            f'Error en la busqueda de la url: {url}, respuesta del servidor: {response.text}')
    return result


def get_combinations_json(sku):
    url = JSON_COMBINATIONS_BY_REFERENCE + sku
    data = get_data_json(url)
    return data


def existe_en_prestashop(sku):
    url = JSON_PRODUCTS_BY_REFERENCE + sku
    data = get_data_json(url)
    return data


def get_product_xml(url, idProduct):
    url = url + str(idProduct) + '&output_format=XML'
    data = get_data_xml(url)

    return data


def update_quantity_xml(xml_string, new_quantity):
    # Convertir el string XML a bytes
    xml_bytes = xml_string.encode("UTF-8")

    # Parsear los bytes XML
    root = etree.fromstring(xml_bytes)

    # Buscar la etiqueta 'quantity' y actualizar su texto con el nuevo valor
    quantity_tag = root.find(".//quantity")
    if quantity_tag is not None:
        quantity_tag.text = str(new_quantity)

    # Convertir el XML actualizado de nuevo a string
    updated_xml = etree.tostring(
        root, encoding="UTF-8", pretty_print=True, xml_declaration=True).decode("UTF-8")

    return updated_xml

    # # Parsear el string XML
    # xml_string = xml_string.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
    # root = ET.fromstring(xml_string)

    # # Buscar la etiqueta 'quantity' y actualizar su texto con el nuevo valor
    # quantity_tag = root.find(".//quantity")
    # if quantity_tag is not None:
    #     quantity_tag.text = str(new_quantity)

    # # Convertir el XML actualizado de nuevo a string
    # updated_xml = ET.tostring(root, encoding="UTF-8").decode("UTF-8")

    # return updated_xml


def put_data(parametros, url):
    # # Codificar el XML en UTF-8
    # data = parametros.encode('utf-8')
    response = requests.put(url, auth=(PRESTASHOP_KEY, ''),
                            headers=HEADERS_XML, data=parametros)
    result = {'status': False, 'response': None}
    if response.status_code == 200:
        result['status'] = True
        result['response'] = response.text

    else:
        print(f'Error: {response.status_code} Mensaje: {response.text}')

    return result


def update_xml(xml_string, url, idProduct):
    url = url + str(idProduct)

    response = put_data(xml_string, url)
    return response

def get_id_stock(url,ProductId):
    url = url + str(ProductId)
    response = get_data_json(url)
    return response
