import os, requests, json, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class ShopifyConnection:
    def __init__(self, shop_url, api_password, api_version="2024-01"):
        self.shop_url = shop_url
        self.api_password = api_password
        self.api_version = api_version
        self.base_url = f"{self.shop_url}/admin/api/{self.api_version}/"

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.api_password
        }


