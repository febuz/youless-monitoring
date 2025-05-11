import requests
import json
import csv
import time
import os
from datetime import datetime

# Configuratie
YOULESS_IP = "192.168.1.20"  # IP van uw Youless
INTERVAL = 60  # Interval in seconden tussen metingen
DATA_DIR = "youless_data"  # Map om data op te slaan

# Zorg dat de data map bestaat
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Maak CSV bestand met headers voor de huidige dag
def get_csv_file():
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = os.path.join(DATA_DIR, f"youless_data_{date_str}.csv")
    
    # Maak nieuw bestand aan als het nog niet bestaat
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Timestamp', 'DateTime', 
                'Net_kWh', 'Power_W', 
                'Consumption_kWh', 'Consumption_W',
                'LowTariff_kWh', 'HighTariff_kWh', 
                'LowReturn_kWh', 'HighReturn_kWh',
                'Current_L1', 'Current_L2', 'Current_L3',
                'Voltage_L1', 'Voltage_L2', 'Voltage_L3',
                'Power_L1', 'Power_L2', 'Power_L3'
            ])
    
    return filename

def log_data():
    try:
        # Haal basis energiegegevens op
        response_e = requests.get(f"http://{YOULESS_IP}/e?f=j")
        data_e = json.loads(response_e.text)[0]
        
        # Haal faseinformatie op
        response_f = requests.get(f"http://{YOULESS_IP}/f")
        data_f = json.loads(response_f.text)
        
        # Genereer timestamp en datum/tijd string
        timestamp = int(time.time())
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Haal alle benodigde waarden op (met foutafhandeling)
        net_kwh = data_e.get("net", 0)
        power_w = data_e.get("pwr", 0)
        consumption_kwh = data_e.get("cs0", 0)
        consumption_w = data_e.get("ps0", 0)
        low_tariff = data_e.get("p1", 0)
        high_tariff = data_e.get("p2", 0)
        low_return = data_e.get("n1", 0)
        high_return = data_e.get("n2", 0)
        
        # Faseinformatie
        current_l1 = data_f.get("i1", 0)
        current_l2 = data_f.get("i2", 0)
        current_l3 = data_f.get("i3", 0)
        voltage_l1 = data_f.get("v1", 0)
        voltage_l2 = data_f.get("v2", 0)
        voltage_l3 = data_f.get("v3", 0)
        power_l1 = data_f.get("l1", 0)
        power_l2 = data_f.get("l2", 0)
        power_l3 = data_f.get("l3", 0)
        
        # Schrijf naar CSV
        csv_file = get_csv_file()
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp, dt_string,
                net_kwh, power_w,
                consumption_kwh, consumption_w,
                low_tariff, high_tariff,
                low_return, high_return,
                current_l1, current_l2, current_l3,
                voltage_l1, voltage_l2, voltage_l3,
                power_l1, power_l2, power_l3
            ])
        
        print(f"[{dt_string}] Data gelogd - Vermogen: {power_w}W, Spanning: {voltage_l1}/{voltage_l2}/{voltage_l3}V")
        
    except Exception as e:
        print(f"Fout bij het loggen van data: {e}")

def main():
    print(f"Youless Logger gestart - Data wordt opgeslagen in de map '{DATA_DIR}'")
    print(f"Verbinding met Youless op {YOULESS_IP}, logging interval: {INTERVAL} seconden")
    
    try:
        while True:
            log_data()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nProgramma gestopt door gebruiker")

if __name__ == "__main__":
    main()