import sys, json
sys.path.append('/home/snparada/Spacionatural/Libraries')
from shopify_lib.products import ShopifyProducts
from laudus_lib.products import LaudusProducts


def leer_stock_json(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        data = json.load(archivo)
    return data["products"]


# ruta donde tiene que ir el json
stocks_in_laudus_path = '/home/snparada/Spacionatural/E-Commerce/Stock_Laudus_to_Shopify/shopify/data/stock_product_laudus.json'

# Crear una instancia de read_stock_product
stock_prod = LaudusProducts()
stock_prod.read_stock_product('008',stocks_in_laudus_path)

# Crear una instancia de ProductOperations
product_ops = ShopifyProducts()

productos = product_ops.read_all_products()

shopify_products_path = '/home/snparada/Spacionatural/E-Commerce/Stock_Laudus_to_Shopify/shopify/data/productos_shopify.json'

product_ops.export_products_to_json(productos,shopify_products_path)


# Carga los archivos JSON
with open(stocks_in_laudus_path, 'r') as file:
    laudus_stock_data = json.load(file)

with open(shopify_products_path, 'r') as file:
    productos_shopify = json.load(file)


# Bucle para buscar y actualizar stock
for stock_item in laudus_stock_data["products"]:
    sku_to_find = stock_item["sku"]
    new_stock = stock_item["stock"]
    for producto in productos_shopify:
        for variante in producto["variants"]:
            if variante["sku"] == sku_to_find:
                inventory_item_id = variante["inventory_item_id"]
                product_ops.update_stock(inventory_item_id, new_stock,sku_to_find)
