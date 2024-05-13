import sys
sys.path.append('/home/snparada/Spacionatural/Libraries/prestashop_lib/database')
from orders import OrderDatabase
import pandas as pd

orders = OrderDatabase()

all_orders_states = orders.read_all_history_orders()
all_orders = orders.read_all_orders()

all_orders = all_orders.drop(columns=['id_shop_group','id_shop','id_lang','id_currency','secure_key','recyclable','gift','gift_message'])
all_orders = all_orders[all_orders['valid']==1]

all_orders_states.to_csv('/home/snparada/Spacionatural/Data/Historical/historic_orders_states_prestashop.csv',index=False)
all_orders.to_csv('/home/snparada/Spacionatural/Data/Historical/historic_orders_prestashop_without_items.csv',index=False)

orders_with_detailed = orders.read_all_orders_with_detailed()
orders_with_detailed.to_csv('/home/snparada/Spacionatural/Data/Historical/historic_orders_prestashop_with_detailed.csv', index=False)