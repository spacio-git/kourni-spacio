# product_operations.py en la carpeta products

import requests, json, time


class ProductOperations:
    def __init__(self, shopify_connection):
        self.shopify_connection = shopify_connection

    def get_products(self):
        endpoint = 'products.json'
        response = requests.get(self.shopify_connection.base_url + endpoint, headers=self.shopify_connection.get_headers())

        # Verifica si la respuesta es válida y tiene contenido
        if response.status_code == 200 and response.content:
            return json.loads(response.content)
        else:
            # Manejar respuesta vacía o error
            print(f"Error al obtener productos: {response.status_code}, {response.text}")
            return None    

    def obtener_id_ubicacion(self):
        url_ubicaciones = f"{self.shopify_connection.base_url}locations.json"
        respuesta = requests.get(url_ubicaciones, headers=self.shopify_connection.get_headers())
        ubicaciones = json.loads(respuesta.content)["locations"]
        if ubicaciones:
            # Devuelve el ID de la primera ubicación
            return ubicaciones[0]["id"]
        else:
            return None


    def actualizar_stock(self, stock_data):
        id_ubicacion = self.obtener_id_ubicacion()
        if id_ubicacion is None:
            print("No se encontraron ubicaciones de inventario.")
            return        

        TAMAÑO_BLOQUE = 1  # Número de productos a actualizar en cada bloque
        INTERVALO = 1       # Intervalo en segundos entre bloques

        for i,producto_json in enumerate(stock_data):
            sku_json = producto_json["sku"]
            nuevo_stock = producto_json["stock"]
            sku_encontrado = False  # Bandera para rastrear si se encontró el SKU

            for producto_shopify in self.get_products()["products"]:
                for variante in producto_shopify["variants"]:
                    if variante["sku"] == sku_json:
                        sku_encontrado = True  # SKU encontrado, actualizar bandera
                        id_variante = variante["id"]
                        url_nivel_inventario = f"{self.shopify_connection.base_url}inventory_levels/set.json"
                        datos_actualizacion = {
                            "location_id": id_ubicacion,
                            "inventory_item_id": variante["inventory_item_id"],
                            "available": nuevo_stock
                        }

                        respuesta = requests.post(url_nivel_inventario, json=datos_actualizacion, headers=self.shopify_connection.get_headers())

                        if respuesta.status_code == 200:
                            print(f"Stock actualizado para SKU {sku_json}")
                        if respuesta.status_code == 429 or (500 <= respuesta.status_code < 600):
                            # Límite de tasa alcanzado o error del servidor, espera y reintenta
                            print(f"Error {respuesta.status_code} al actualizar SKU {sku_json}. Reintentando...")
                            time.sleep(10)  # Espera 10 segundos antes de reintentar
                            continue  # Reintenta con el mismo SKU

                        if respuesta.status_code != 200:
                            print(f"Error al actualizar el stock para SKU {sku_json}: {respuesta.text}")
                            # Opcional: decidir si continuar o detener en caso de otro tipo de error

                        # Pausa después de cada bloque de TAMAÑO_BLOQUE iteraciones
                        if (i + 1) % TAMAÑO_BLOQUE == 0:
                            print('durmiendo...')
                            time.sleep(INTERVALO)

                if sku_encontrado:
                    break  # Salir del bucle de productos si se encontró el SKU

            if not sku_encontrado:
                print(f"SKU no encontrado: {sku_json}")
                # Pausa después de cada bloque de TAMAÑO_BLOQUE iteraciones
                if (i + 1) % TAMAÑO_BLOQUE == 0:
                    print('durmiendo...')
                    time.sleep(INTERVALO)
               

