#!/bin/bash

# Ruta del archivo de registro (log)
log_file="/home/snparada/Spacionatural/Others/Logs/run_11_15_19.log"

# Ejecutar createLaudusToken.py
echo "LaudusTokenLogs:" >> "$log_file"
python3 /home/snparada/Spacionatural/Libraries/laudus_lib/creds/createLaudusToken.py >> "$log_file" 2>&1
echo "" >> "$log_file"

# Ejecutar Sincronizacion Stock Laudus 
echo "Stock_Laudus_to_Shopi:" >> "$log_file"
python3 /home/snparada/Spacionatural/E-Commerce/Stock_Laudus_to_Shopify/shopify/index.py >> "$log_file" 2>&1
echo "" >> "$log_file"