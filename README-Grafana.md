# Youless Monitoring Systeem met Grafana

Dit is een uitgebreid systeem voor het monitoren van één of meerdere Youless energiemeters met realtime visualisatie in Grafana.

## Inhoudsopgave
1. [Systeemoverzicht](#systeemoverzicht)
2. [Benodigdheden](#benodigdheden)
3. [Installatie](#installatie)
4. [Configuratie](#configuratie)
5. [Starten van het systeem](#starten-van-het-systeem)
6. [Grafana Dashboard](#grafana-dashboard)
7. [Meerdere Youless-apparaten](#meerdere-youless-apparaten)
8. [Probleemoplossing](#probleemoplossing)

## Systeemoverzicht

Dit systeem bestaat uit drie hoofdcomponenten:

1. **Data Collector**: Een Python-script dat data ophaalt van Youless apparaten en opslaat in InfluxDB
2. **InfluxDB**: Een tijdreeksdatabase voor het opslaan van meetgegevens
3. **Grafana**: Een visualisatietool voor het maken van dashboards

Met deze setup kunt u:
- Gegevens verzamelen van meerdere Youless-apparaten
- Historische data opslaan en analyseren
- Realtime grafieken en dashboards weergeven
- Alarmen instellen bij afwijkende waarden

## Benodigdheden

- Windows 10 of 11
- Python 3.7 of hoger
- Docker Desktop (voor InfluxDB en Grafana)
- Eén of meerdere Youless energiemeters in uw netwerk

## Installatie

### Stap 1: Voorbereidingen

1. Download en installeer [Python](https://www.python.org/downloads/windows/)
   - Zorg ervoor dat u "Add Python to PATH" aanvinkt tijdens de installatie
2. Download en installeer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Start Docker Desktop na de installatie

### Stap 2: Installatie van het monitoringsysteem

1. Voer het bestand `install.bat` uit
   - Dit installeert de benodigde Python-packages
   - Dit maakt de benodigde mappen aan
2. Controleer of alle onderdelen correct zijn geïnstalleerd

## Configuratie

### Configuratie van de Data Collector

Open het bestand `config.yaml` in een tekstverwerker en pas de volgende instellingen aan:

```yaml
influxdb:
  host: localhost
  port: 8086
  username: youless
  password: password
  database: youless_metrics

devices:
  - name: main
    ip: 192.168.1.20  # Pas dit aan naar het IP van uw Youless
    interval: 10
    enabled: true
  # Voeg hier meer apparaten toe indien nodig
  # - name: tweede_meter
  #   ip: 192.168.1.21
  #   interval: 10
  #   enabled: true

collection:
  interval: 10  # seconden tussen metingen
  retry_interval: 30  # seconden wachten na mislukte poging
  max_retries: 3  # maximum aantal pogingen per cyclus
```

## Starten van het systeem

### Stap 1: Start InfluxDB en Grafana

Open een Command Prompt in de installatiemap en voer uit:

```
docker-compose up -d
```

Dit start de containers voor InfluxDB en Grafana op de achtergrond.

### Stap 2: Start de Data Collector

Voer het bestand `start_collector.bat` uit of gebruik de volgende opdracht:

```
python youless_to_influxdb.py
```

De collector begint nu gegevens op te halen van uw Youless apparaten en deze op te slaan in InfluxDB.

## Grafana Dashboard

1. Open Grafana in uw webbrowser: http://localhost:3000
2. Log in met de standaard inloggegevens:
   - Gebruikersnaam: `admin`
   - Wachtwoord: `admin`
3. Bij de eerste keer inloggen wordt u gevraagd om het wachtwoord te wijzigen

Het vooraf geconfigureerde Youless dashboard zou automatisch beschikbaar moeten zijn onder Dashboards > Youless.

## Meerdere Youless-apparaten

Om meerdere Youless-apparaten te monitoren:

1. Bewerk het bestand `config.yaml`
2. Voeg nieuwe apparaten toe in de `devices` sectie:

```yaml
devices:
  - name: main
    ip: 192.168.1.20
    interval: 10
    enabled: true
  - name: bijgebouw
    ip: 192.168.1.21
    interval: 10
    enabled: true
  - name: garage
    ip: 192.168.1.22
    interval: 10
    enabled: true
```

3. Herstart de Data Collector
4. De gegevens van alle apparaten worden automatisch opgeslagen in InfluxDB en zijn beschikbaar in Grafana

## Probleemoplossing

### Data Collector werkt niet

1. Controleer of u het juiste IP-adres hebt ingesteld in `config.yaml`
2. Controleer of de Youless bereikbaar is door te pingen: `ping 192.168.1.20`
3. Controleer de log voor foutmeldingen

### InfluxDB of Grafana niet beschikbaar

1. Controleer of Docker draait
2. Controleer de status van de containers: `docker ps`
3. Herstart de containers indien nodig: `docker-compose restart`

### Youless API foutmeldingen

Zorg ervoor dat uw Youless firmware up-to-date is. Sommige oudere versies ondersteunen mogelijk niet alle API-eindpunten die worden gebruikt door de collector.

---

## Geavanceerde mogelijkheden

- **Alarmen instellen**: Configureer alarmen in Grafana voor specifieke drempelwaarden
- **Automatisch opstarten**: Voeg snelkoppelingen toe aan de Windows Opstartmap
- **Data-export**: Gebruik InfluxDB tools om langetermijngegevens te exporteren en analyseren