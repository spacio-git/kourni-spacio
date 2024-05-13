import sys
sys.path.append('/home/sam/Spacionatural/E-Commerce/')
sys.path.append('/home/sam/Spacionatural/Libraries')

from Sincronizacion_Stock.shopify.connection.shopify_connection import ShopifyConnection
from Sincronizacion_Stock.shopify.products.product_operations import ProductOperations
from Sincronizacion_Stock.shopify.data.data_operations import leer_stock_json
from Sincronizacion_Stock.shopify.creds.config import SHOPIFY_SHOP_URL, SHOPIFY_PASSWORD  
from laudus_lib.products import LaudusProduct


# Crear una instancia de read_stock_product
stock_prod = LaudusProduct()
stock_prod.read_stock_product('008')


# Crear una instancia de ShopifyConnection
conn = ShopifyConnection(SHOPIFY_SHOP_URL, SHOPIFY_PASSWORD)

# Crear una instancia de ProductOperations
product_ops = ProductOperations(conn)

# Leer datos del JSON
ruta_json = "/home/sam/Spacionatural/E-Commerce/Sincronizacion_Stock/shopify/data/stock_product_laudus.json"
datos_stock = leer_stock_json(ruta_json)


# Actualizar stock en Shopify
product_ops.actualizar_stock(datos_stock)