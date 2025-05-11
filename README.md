# Youless Energiemeter Logger en Visualisatie

Dit is een eenvoudig systeem om gegevens van een Youless energiemeter (LS120) op te slaan en te visualiseren.

## Bestanden

- `youless_logger.py` - Script dat periodiek data ophaalt van de Youless en opslaat in CSV bestanden
- `youless_visualizer.py` - Script dat grafieken maakt van de verzamelde data

## Installatie op Windows

### Benodigdheden

1. Python 3.7 of hoger: [Download Python](https://www.python.org/downloads/windows/)
2. Vereiste Python packages

### Stap 1: Python installeren

1. Download Python van de officiële website
2. Voer het installatieprogramma uit
3. Zorg ervoor dat je aanvinkt: "Add Python to PATH"

### Stap 2: Benodigde packages installeren

Open de Command Prompt (cmd) en voer uit:

```
pip install requests pandas matplotlib
```

## Gebruik

### Stap 1: Configuratie

Open `youless_logger.py` en pas indien nodig deze instellingen aan:

```python
YOULESS_IP = "192.168.1.20"  # Pas aan naar het juiste IP-adres
INTERVAL = 60  # Interval in seconden tussen metingen
DATA_DIR = "youless_data"  # Map om data op te slaan
```

### Stap 2: Data verzamelen

1. Maak een map `youless_data` in dezelfde map als de scripts
2. Start het logging script:

```
python youless_logger.py
```

Dit script blijft draaien en slaat elke minuut (of volgens ingesteld interval) de data op in CSV-bestanden, één bestand per dag.

### Stap 3: Grafieken maken

Nadat je data hebt verzameld, kun je grafieken maken met:

```
python youless_visualizer.py
```

Dit maakt grafieken van:
- Totaal vermogen
- Spanning per fase
- Stroomsterkte per fase
- Vermogen per fase

De grafieken worden opgeslagen in de map `youless_graphs`.

## Automatisch opstarten (Windows)

Om het logging script automatisch te starten bij het opstarten van Windows:

1. Maak een .bat bestand (bijv. `start_youless_logger.bat`) met de volgende inhoud:
```
@echo off
cd /d %~dp0
python youless_logger.py
```

2. Plaats een snelkoppeling naar dit .bat bestand in de map "Opstarten":
   - Druk op `Win + R`
   - Typ `shell:startup` en druk op Enter
   - Kopieer de snelkoppeling naar dit venster

## Geavanceerde visualisatie

Voor geavanceerdere visualisatie kun je ook tools gebruiken zoals:

1. **Grafana**: Zeer geavanceerde dashboards
2. **Power BI**: Voor uitgebreide rapportages
3. **Excel**: Voor eenvoudige grafieken en analyses van de CSV-bestanden

## De Youless data begrijpen

De belangrijkste waarden die worden opgeslagen:

- **Net_kWh**: Netto energieverbruik (negatief bij teruglevering)
- **Power_W**: Momenteel vermogen (Watt)
- **Consumption_kWh**: Totaal verbruik
- **Consumption_W**: Momenteel verbruik (Watt)
- **Current_L1/L2/L3**: Stroomsterkte per fase (Ampère)
- **Voltage_L1/L2/L3**: Spanning per fase (Volt)
- **Power_L1/L2/L3**: Vermogen per fase (Watt)