import time
import pytz
import sys
sys.path.append('/home/snparada/Spacionatural/E-Commerce/Stock_Laudus_to_Shopify')
from api.urls import STOCK_BY_WAREHOUSEID
from api.methods.Laudus import get_stock
from api.methods.Prestashop import get_combinations_json, existe_en_prestashop, get_product_xml, update_quantity_xml, update_xml,get_id_stock,get_data_json
from helpers.validations import esta_vacio
from api.urls import XML_STOCK_AVAILABLES, XML_STOCK_AVAILABLES_BY_ID_PRODUCT_ATTRIBUTE, JSON_STOCK_AVAILABLES_BY_ID_PRODUCT_ATTRIBUTE,JSON_STOCK_AVAILABLES_BY_ID_PRODUCT
from datetime import datetime

def process_stock():

    # Define la zona horaria para Santiago
    santiago_tz = pytz.timezone('Chile/Continental')
    # Obtiene la hora actual en UTC y la convierte a la zona horaria de Santiago
    current_time = datetime.now(santiago_tz)
    jsonStockLaudus = get_stock(STOCK_BY_WAREHOUSEID)

    if (jsonStockLaudus['status']):
        products = jsonStockLaudus['response']['products']
        for product in products:
            # Convertir el valor de 'stock' a un entero
            product['stock'] = int(product['stock'])

            # if str(product['sku']) == '8104':

            print(product)
            # validamos si tiene combinaciones
            jsonCombinationsPrestashop = get_combinations_json(product['sku'])
            if (jsonCombinationsPrestashop['status']):
                tieneCombinaciones = esta_vacio(
                    jsonCombinationsPrestashop['response'])
                if (tieneCombinaciones):
                    print(
                        f'el producto con sku {product["sku"]} no tiene combinaciones')
                    print('Validamos que el sku exista en prestashop')
                    estaEnPrestashop = existe_en_prestashop(product['sku'])
                    print(estaEnPrestashop)
                    if (estaEnPrestashop['status']):
                        estaVacio = esta_vacio(estaEnPrestashop['response'])
                        # print(estaVacio)
                        if (estaVacio == False):
                            print('el sku esta en prestashop')

                            #obtenemos el id del stock del sku en prestashop
                            stock_available = get_data_json(JSON_STOCK_AVAILABLES_BY_ID_PRODUCT+ str(estaEnPrestashop['response']['products'][0]['id']) )
                            # print (stock_available)
                            # actualizamos el stock del laudus en el prestashop
                            productPrestashop = get_product_xml(XML_STOCK_AVAILABLES,
                                                                stock_available['response']['stock_availables'][0]['id'])
                            # print(productPrestashop)
                            if (productPrestashop['status']):
                                updated_xml = update_quantity_xml(
                                    productPrestashop['response'], product['stock'])
                                # print (updated_xml)

                                isUpdatedXML = update_xml(
                                    updated_xml, XML_STOCK_AVAILABLES, estaEnPrestashop['response']['products'][0]['id'])
                                # print(isUpdatedXML)
                                if (isUpdatedXML['status']):
                                    
                                    print(    
                                        f"el producto {product['sku']} fue actualizado en prestashop, {current_time.strftime('%Y-%m-%d %H:%M:%S')}" )
                                else:
                                    print(
                                        f"hubo un problema con el producto {product['sku']} la momento de actualizar, {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        else:
                            print('el sku no esta en prestashop')

                else:
                    print(
                        f'el producto con sku {product["sku"]} si tiene combinaciones')

                    print(jsonCombinationsPrestashop['response'])

                    combinationId = jsonCombinationsPrestashop['response']['combinations'][0]['id']

                    # print(productPrestashop)
                    getIdStockAvailables = get_id_stock(JSON_STOCK_AVAILABLES_BY_ID_PRODUCT_ATTRIBUTE,combinationId)
                    # print(getIdStockAvailables)
                    productPrestashop = get_product_xml(
                        XML_STOCK_AVAILABLES, getIdStockAvailables['response']['stock_availables'][0]['id'])
                    # print(productPrestashop)

                    if (productPrestashop['status']):
                        updated_xml = update_quantity_xml(
                            productPrestashop['response'], product['stock'])
                        # print(updated_xml)

                        isUpdatedXML = update_xml(
                            updated_xml, XML_STOCK_AVAILABLES_BY_ID_PRODUCT_ATTRIBUTE, combinationId)
                        if(isUpdatedXML):
                            print(f"el sku {product['sku']} se actualizo correctamente, {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

                print('------------------------------------')
            
            # time.sleep(3)
