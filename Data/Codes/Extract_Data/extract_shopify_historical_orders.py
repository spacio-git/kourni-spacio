import sys, json
import pandas as pd
sys.path.append('/home/snparada/Spacionatural/Libraries')
dotenv_path = '/home/snparada/Spacionatural/Libraries/shopify_lib/creds/.env'
config = Config(RepositoryEnv(dotenv_path))

print('since_id', config('SINCE_ID'))
config('SINCE_ID') = 123123
print('since_id', config('SINCE_ID'))


from shopify_lib.orders import ShopifyOrders

shopify_orders_obj = ShopifyOrders()
all_shopify_orders = shopify_orders_obj.read_last_order()

def main():
    order = []
    order_number = []
    customer_name = []
    customer_last_name = []
    email = []
    mobile = []
    address = []
    comuna = []
    region = []
    rut = []
    document_type = []
    delivery_name = []
    delivery_amout = []
    invoice_address = []
    invoice_rut = []
    invoice_razon = []
    invoice_giro = []
    invoice_comuna = []
    invoice_region = []
    payment_method = []
    items_number = []
    cart = []

    index = 0
    for shopify_order in all_shopify_orders:
        index = index + 1
        order.append(index)
        order_number.append(shopify_order['name'])
        customer_name.append(shopify_order['customer']['first_name'])
        customer_last_name.append(shopify_order['customer']['last_name'])
        email.append(shopify_order['customer']['email'])
        mobile.append(shopify_order['customer']['phone'])
        address.append(shopify_order['customer']['default_address']['address1'])
        comuna.append(shopify_order['customer']['default_address']['city'])
        region.append(shopify_order['customer']['default_address']['province'])
        rut.append(shopify_order['customer']['default_address']['zip'])
        temp_document_type = ''
        temp_invoice_rut = ''
        temp_invoice_razon = ''
        temp_invoice_giro = ''
        for note_attribute in shopify_order['note_attributes']:
            if note_attribute['name'] == 'shoppingcart-tags':
                temp_document_type = note_attribute['value']
            elif note_attribute['name'] == 'RUT':
                temp_invoice_rut = note_attribute['value']
            elif note_attribute['name'] == 'razon':
                temp_invoice_razon = note_attribute['value']
            elif note_attribute['name'] == 'giro':
                temp_invoice_giro = note_attribute['value']
        document_type.append(temp_document_type)
        invoice_razon.append(temp_invoice_razon)
        invoice_giro.append(temp_invoice_giro)
        temp_delivery_name = None
        try:
            temp_delivery_name = shopify_order['shipping_lines'][0]['title']
        except:
            temp_delivery_name = ''
        temp_delivery_amount = None
        try:
            temp_delivery_amount = shopify_order['shipping_lines'][0]['price']
        except:
            temp_delivery_amount = ''
        delivery_name.append(temp_delivery_name)
        delivery_amout.append(temp_delivery_amount)
        invoice_address.append(shopify_order['billing_address']['address1'])
        invoice_rut.append(shopify_order['billing_address']['zip'])
        invoice_comuna.append(shopify_order['billing_address']['city'])
        invoice_region.append(shopify_order['billing_address']['province'])
        payment_method.append(shopify_order['payment_gateway_names'][0])
        count = 0
        temp_cart = '['
        for line_item in shopify_order['line_items']:
            count = count + int(line_item['quantity'])
            temp_cart = temp_cart + "{" + str(line_item['sku']) + ', ' + str(line_item['quantity']) + "}"
        temp_cart = f"{temp_cart}]"
        cart.append(temp_cart)
        items_number.append(count)

    data = {
        'order': order,
        'order_number': order_number,
        'customer_name': customer_name,
        'customer_last_name': customer_last_name,
        'email': email,
        'mobile': mobile,
        'address': address,
        'comuna': comuna,
        'region': region,
        'rut': rut,
        'document_type': document_type,
        'customer_name': customer_name,
        'delivery_name': delivery_name,
        'delivery_amout': delivery_amout,
        'invoice_address': invoice_address,
        'invoice_rut': invoice_rut,
        'invoice_razon': invoice_razon,
        'invoice_giro': invoice_giro,
        'invoice_comuna': invoice_comuna,
        'invoice_region': invoice_region,
        'payment_method': payment_method,
        'items_number': items_number,
        'cart': cart
    }
    df = pd.DataFrame(data)
    return df


result = main()
print(result.tail().T)
result.to_csv('/home/snparada/Spacionatural/Data/Historical/historic_customers_shopify.csv', index = False)