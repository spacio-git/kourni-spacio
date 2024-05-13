
import sys
sys.path.append('/home/snparada/Spacionatural/Libraries/shopify_lib')
from api import ShopifyAPI
import requests, json, time
from urllib.parse import quote,urljoin, urlparse


class ShopifyProducts(ShopifyAPI):
    def __init__(self, shop_url=None, api_password=None, api_version="2024-01"):
        super().__init__(shop_url, api_password, api_version)

# CRUD      
    
    def read_all_products(self):       
        products = []
        endpoint = 'products.json?limit=250'
        while endpoint:
            full_url = urljoin(self.base_url, endpoint)
            response = requests.get(full_url, headers=self.get_headers())

            if response.status_code == 200 and response.content:
                data = json.loads(response.content)
                products.extend(data['products'])

                next_link = response.links.get('next')
                if next_link:
                    next_url = next_link['url']
                    parsed_url = urlparse(next_url)
                    endpoint = parsed_url.path + "?" + parsed_url.query
                else:
                    endpoint = None
            else:
                print(f"Error al obtener productos: {response.status_code}, {response.text}")
                break

        return products
    
    def read_location_id(self, inventory_item_id):
        endpoint = f"inventory_levels.json?inventory_item_ids={inventory_item_id}"
        # Construye la URL completa usando self.base_url
        inventory_url = urljoin(self.base_url, endpoint)

        # Realiza la petición GET usando self.get_headers() para incluir las cabeceras correctas
        response = requests.get(inventory_url, headers=self.get_headers())

        if response.status_code == 200:
            inventory_data = response.json()["inventory_levels"]
            if inventory_data:
                return inventory_data[0]["location_id"]
            else:
                print(f"No se encontraron niveles de inventario para el inventory_item_id {inventory_item_id}")
                return None
        else:
            print(f"Error al obtener location_id para inventory_item_id {inventory_item_id}: {response.status_code} - {response.text}")
            return None
   
    def update_stock(self, inventory_item_id, new_stock, sku):
        location_id = self.read_location_id(inventory_item_id)
        if location_id:
            # Usa self.base_url para construir la URL completa
            update_url = urljoin(self.base_url, "inventory_levels/set.json")
            
            data = {
                "location_id": location_id,
                "inventory_item_id": inventory_item_id,
                "available": new_stock
            }
            # Usa self.get_headers() para obtener las cabeceras correctas
            response = requests.post(update_url, json=data, headers=self.get_headers())
            if response.status_code == 200:
                print(f"Stock actualizado para SKU {sku}.")
            else:
                print(f"Error al actualizar stock para SKU {sku}: {response.status_code} - {response.text}")
        else:
            print(f"No se pudo obtener el location_id para inventory_item_id {inventory_item_id}")

        # Espera para evitar saturar la API o violar los límites de la tasa de solicitud
        time.sleep(3)

    def update_price(self, variant_id, new_price,sku):
        update_url = f"{self.shopify_connection.base_url}/variants/{variant_id}.json"
        data = {
            "variant": {
                "id": variant_id,
                "price": new_price
            }
        }
        response = requests.put(update_url, json=data, headers=self.shopify_connection.get_headers())
        if response.status_code == 200:
            print(f"Precio actualizado para el sku {sku}")
        else:
            print(f"Error al actualizar el precio para el {sku}: {response.text}")

        # Pausa después de cada actualización
        print("durmiendo...")
        time.sleep(3)
               
# AUX Functions

    def export_products_to_json(self, products,path):        
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(products, file, ensure_ascii=False, indent=4)

