import requests
import json
import time
from datetime import datetime
from influxdb import InfluxDBClient
import logging
import sys
import os
import yaml

# Logging configuratie
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("youless_collector.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# Standaard configuratie
DEFAULT_CONFIG = {
    "influxdb": {
        "host": "localhost",
        "port": 8086,
        "username": "youless",
        "password": "password",
        "database": "youless_metrics"
    },
    "devices": [
        {
            "name": "main",
            "ip": "192.168.1.20", 
            "interval": 10,
            "enabled": True
        }
    ],
    "collection": {
        "interval": 10,
        "retry_interval": 30,
        "max_retries": 3
    }
}

# Functie om configuratiebestand te laden
def load_config():
    config_path = "config.yaml"
    
    # Aanmaken van standaard configuratie als er geen bestand is
    if not os.path.exists(config_path):
        logger.info("Geen configuratiebestand gevonden, standaard configuratie wordt aangemaakt")
        with open(config_path, 'w') as file:
            yaml.dump(DEFAULT_CONFIG, file, default_flow_style=False)
        return DEFAULT_CONFIG
    
    # Bestaand configuratiebestand laden
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuratiebestand geladen: {len(config['devices'])} apparaten gevonden")
            return config
    except Exception as e:
        logger.error(f"Fout bij laden configuratie: {e}")
        logger.info("Terugvallen op standaard configuratie")
        return DEFAULT_CONFIG

# Functie om InfluxDB-client aan te maken
def create_influxdb_client(config):
    try:
        db_config = config['influxdb']
        client = InfluxDBClient(
            host=db_config['host'],
            port=db_config['port'],
            username=db_config['username'],
            password=db_config['password'],
            database=db_config['database']
        )
        
        # Database aanmaken als deze niet bestaat
        dbs = client.get_list_database()
        if not any(db['name'] == db_config['database'] for db in dbs):
            logger.info(f"Database '{db_config['database']}' wordt aangemaakt")
            client.create_database(db_config['database'])
        
        client.switch_database(db_config['database'])
        return client
    except Exception as e:
        logger.error(f"Fout bij verbinden met InfluxDB: {e}")
        return None

# Functie om data van Youless op te halen
def get_youless_data(device):
    device_ip = device['ip']
    device_name = device['name']
    
    try:
        # Basisgegevens ophalen
        response_e = requests.get(f"http://{device_ip}/e?f=j", timeout=5)
        data_e = json.loads(response_e.text)[0]
        
        # Faseinformatie ophalen
        response_f = requests.get(f"http://{device_ip}/f", timeout=5)
        data_f = json.loads(response_f.text)
        
        # Combineer de gegevens
        data = {
            "device_name": device_name,
            "device_ip": device_ip,
            "timestamp": int(time.time()),
            "net_kwh": data_e.get("net", 0),
            "power_w": data_e.get("pwr", 0),
            "consumption_kwh": data_e.get("cs0", 0),
            "consumption_w": data_e.get("ps0", 0),
            "low_tariff": data_e.get("p1", 0),
            "high_tariff": data_e.get("p2", 0),
            "low_return": data_e.get("n1", 0),
            "high_return": data_e.get("n2", 0),
            "current_l1": data_f.get("i1", 0),
            "current_l2": data_f.get("i2", 0),
            "current_l3": data_f.get("i3", 0),
            "voltage_l1": data_f.get("v1", 0),
            "voltage_l2": data_f.get("v2", 0),
            "voltage_l3": data_f.get("v3", 0),
            "power_l1": data_f.get("l1", 0),
            "power_l2": data_f.get("l2", 0),
            "power_l3": data_f.get("l3", 0)
        }
        
        logger.debug(f"Data opgehaald van {device_name} ({device_ip})")
        return data
    
    except Exception as e:
        logger.error(f"Fout bij ophalen data van {device_name} ({device_ip}): {e}")
        return None

# Functie om data naar InfluxDB te schrijven
def write_to_influxdb(client, data):
    if not client or not data:
        return False
    
    try:
        device_name = data["device_name"]
        timestamp = data["timestamp"] * 1000000000  # Omzetten naar nanoseconden voor InfluxDB
        
        # Data voorbereiden voor InfluxDB
        points = [
            {
                "measurement": "power",
                "tags": {
                    "device": device_name,
                    "ip": data["device_ip"]
                },
                "time": timestamp,
                "fields": {
                    "net_kwh": float(data["net_kwh"]),
                    "power_w": float(data["power_w"]),
                    "consumption_kwh": float(data["consumption_kwh"]),
                    "consumption_w": float(data["consumption_w"]),
                    "low_tariff": float(data["low_tariff"]),
                    "high_tariff": float(data["high_tariff"]),
                    "low_return": float(data["low_return"]),
                    "high_return": float(data["high_return"])
                }
            },
            {
                "measurement": "electricity",
                "tags": {
                    "device": device_name,
                    "ip": data["device_ip"]
                },
                "time": timestamp,
                "fields": {
                    "current_l1": float(data["current_l1"]),
                    "current_l2": float(data["current_l2"]),
                    "current_l3": float(data["current_l3"]),
                    "voltage_l1": float(data["voltage_l1"]),
                    "voltage_l2": float(data["voltage_l2"]),
                    "voltage_l3": float(data["voltage_l3"]),
                    "power_l1": float(data["power_l1"]),
                    "power_l2": float(data["power_l2"]),
                    "power_l3": float(data["power_l3"])
                }
            }
        ]
        
        # Schrijf naar database
        success = client.write_points(points)
        if success:
            logger.debug(f"Data geschreven naar InfluxDB voor {device_name}")
        else:
            logger.warning(f"Kon data niet schrijven naar InfluxDB voor {device_name}")
        
        return success
    
    except Exception as e:
        logger.error(f"Fout bij schrijven naar InfluxDB: {e}")
        return False

# Hoofdfunctie
def main():
    logger.info("Youless to InfluxDB collector gestart")
    
    # Laad configuratie
    config = load_config()
    
    # Maak InfluxDB client
    influx_client = create_influxdb_client(config)
    if not influx_client:
        logger.error("Kon geen verbinding maken met InfluxDB. Programma wordt gestopt.")
        return
    
    logger.info(f"Verbonden met InfluxDB op {config['influxdb']['host']}:{config['influxdb']['port']}")
    
    try:
        # Oneindige lus voor dataverzameling
        while True:
            start_time = time.time()
            
            # Loop door alle geconfigureerde apparaten
            for device in config['devices']:
                if not device.get('enabled', True):
                    continue
                
                try:
                    logger.info(f"Data ophalen van {device['name']} ({device['ip']})")
                    
                    # Probeer data op te halen met herhaalpogingen
                    retries = 0
                    data = None
                    
                    while retries < config['collection']['max_retries']:
                        data = get_youless_data(device)
                        if data:
                            break
                        
                        retries += 1
                        if retries < config['collection']['max_retries']:
                            logger.warning(f"Poging {retries} mislukt voor {device['name']}, opnieuw proberen over {config['collection']['retry_interval']} seconden")
                            time.sleep(config['collection']['retry_interval'])
                    
                    if data:
                        # Schrijf data naar InfluxDB
                        write_to_influxdb(influx_client, data)
                    else:
                        logger.error(f"Kon geen data ophalen van {device['name']} na {retries} pogingen")
                
                except Exception as e:
                    logger.error(f"Onverwachte fout bij apparaat {device['name']}: {e}")
            
            # Bereken en wacht tot het volgende interval
            elapsed = time.time() - start_time
            sleep_time = max(1, config['collection']['interval'] - elapsed)
            
            logger.debug(f"Cyclus voltooid in {elapsed:.2f}s, wachten {sleep_time:.2f}s tot volgende cyclus")
            time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        logger.info("Programma gestopt door gebruiker")
    except Exception as e:
        logger.error(f"Onverwachte fout in hoofdprogramma: {e}")
    finally:
        if influx_client:
            influx_client.close()
        logger.info("Programma beëindigd")

if __name__ == "__main__":
    main()