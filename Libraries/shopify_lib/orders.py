import pandas as pd
import sys
sys.path.append('/home/snparada/Spacionatural/Libraries/')
from shopify_lib.api import ShopifyAPI

class ShopifyOrders(ShopifyAPI):

    def __init__(self, shop_url=None, api_password=None, api_version="2024-01"):
        super().__init__(shop_url, api_password, api_version)

    # CRUD
    def read_last_order(self):
        data = self.read('orders.json', params={'limit': 1, 'order': 'created_at desc'})
        return data['orders'][0] if data['orders'] else None

    def read_all_orders(self, since_id=0, order_status=None):
        datas = []
        params = {}
        if order_status == None:
            params = {'limit': 250, 'since_id': since_id}
        else:
            params = {'limit': 250, 'since_id': since_id, 'status': order_status}
        data = self.read('orders.json', params=params)
        for order in data['orders']:
            since_id = order['id']
            datas.append(order)
        return since_id, datas

        