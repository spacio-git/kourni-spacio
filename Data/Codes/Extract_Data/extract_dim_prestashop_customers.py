import sys
sys.path.append('/home/snparada/Spacionatural/Libraries')
from prestashop_lib.database.customers import CustomerDatabase
import pandas as pd

customers = CustomerDatabase()

customers_df = customers.read_all_customers()

customers_df.to_csv('/home/snparada/Spacionatural/Data/Dim/customers_prestashop.csv', index=False)