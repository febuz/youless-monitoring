import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import glob
from datetime import datetime, timedelta

# Configuratie
DATA_DIR = "youless_data"  # Map met de data
OUTPUT_DIR = "youless_graphs"  # Map voor de grafieken

# Zorg dat de output map bestaat
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data(days=1):
    """Laad data van de afgelopen aantal dagen"""
    all_data = []
    
    # Bepaal welke bestanden we moeten laden
    date_format = "%Y-%m-%d"
    date_list = []
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime(date_format)
        date_list.append(date)
    
    # Zoek de bestanden en laad ze
    for date_str in date_list:
        filename = os.path.join(DATA_DIR, f"youless_data_{date_str}.csv")
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename)
                all_data.append(df)
                print(f"Geladen: {filename} ({len(df)} rijen)")
            except Exception as e:
                print(f"Fout bij laden {filename}: {e}")
    
    # Combineer alle data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        # Converteer DateTime naar datetime object
        combined_df['DateTime'] = pd.to_datetime(combined_df['DateTime'])
        # Sorteer op tijd
        combined_df = combined_df.sort_values('DateTime')
        return combined_df
    else:
        print("Geen data gevonden!")
        return None

def generate_daily_graphs(df, day=None):
    """Genereer grafieken voor een specifieke dag"""
    if df is None or len(df) == 0:
        print("Geen data om grafieken te maken!")
        return
        
    # Filter op de gevraagde dag
    if day is None:
        day = datetime.now().strftime("%Y-%m-%d")
    
    day_start = pd.to_datetime(day)
    day_end = day_start + timedelta(days=1)
    
    day_df = df[(df['DateTime'] >= day_start) & (df['DateTime'] < day_end)]
    
    if len(day_df) == 0:
        print(f"Geen data voor {day}")
        return
    
    print(f"Grafieken maken voor {day} met {len(day_df)} datapunten")
    
    # Maak figuur voor vermogen
    plt.figure(figsize=(12, 6))
    plt.plot(day_df['DateTime'], day_df['Power_W'], label='Vermogen (W)', color='red')
    plt.grid(True, alpha=0.3)
    plt.title(f'Vermogen - {day}')
    plt.xlabel('Tijd')
    plt.ylabel('Watt')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"vermogen_{day}.png"))
    
    # Maak figuur voor stroomsterkte en spanning
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Stroomsterkte
    ax1.plot(day_df['DateTime'], day_df['Current_L1'], label='L1', color='red')
    ax1.plot(day_df['DateTime'], day_df['Current_L2'], label='L2', color='green')
    ax1.plot(day_df['DateTime'], day_df['Current_L3'], label='L3', color='blue')
    ax1.grid(True, alpha=0.3)
    ax1.set_title(f'Stroomsterkte per fase - {day}')
    ax1.set_ylabel('Ampère')
    ax1.legend()
    
    # Spanning
    ax2.plot(day_df['DateTime'], day_df['Voltage_L1'], label='L1', color='red')
    ax2.plot(day_df['DateTime'], day_df['Voltage_L2'], label='L2', color='green')
    ax2.plot(day_df['DateTime'], day_df['Voltage_L3'], label='L3', color='blue')
    ax2.grid(True, alpha=0.3)
    ax2.set_title(f'Spanning per fase - {day}')
    ax2.set_xlabel('Tijd')
    ax2.set_ylabel('Volt')
    ax2.legend()
    
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"spanning_stroom_{day}.png"))
    
    # Maak figuur voor vermogen per fase
    plt.figure(figsize=(12, 6))
    plt.plot(day_df['DateTime'], day_df['Power_L1'], label='L1', color='red')
    plt.plot(day_df['DateTime'], day_df['Power_L2'], label='L2', color='green')
    plt.plot(day_df['DateTime'], day_df['Power_L3'], label='L3', color='blue')
    plt.grid(True, alpha=0.3)
    plt.title(f'Vermogen per fase - {day}')
    plt.xlabel('Tijd')
    plt.ylabel('Watt')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, f"vermogen_per_fase_{day}.png"))
    
    print(f"Grafieken opgeslagen in {OUTPUT_DIR}")

if __name__ == "__main__":
    # Laad data van afgelopen 7 dagen
    data = load_data(days=7)
    
    if data is not None:
        # Maak grafieken voor vandaag
        today = datetime.now().strftime("%Y-%m-%d")
        generate_daily_graphs(data, today)
        
        # Maak ook grafieken voor gisteren
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        generate_daily_graphs(data, yesterday)