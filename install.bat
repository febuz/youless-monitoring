@echo off
echo Youless Monitoring Systeem - Installatie
echo ========================================
echo.

REM Controleer of Python geinstalleerd is
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo FOUT: Python is niet geinstalleerd. Download en installeer Python van https://www.python.org/downloads/windows/
    echo Zorg ervoor dat u "Add Python to PATH" aanvinkt tijdens de installatie.
    pause
    exit /b 1
)

REM Controleer of pip geinstalleerd is
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo FOUT: pip is niet geinstalleerd. Dit zou onderdeel moeten zijn van Python.
    pause
    exit /b 1
)

REM Controleer of Docker geinstalleerd is
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WAARSCHUWING: Docker lijkt niet geinstalleerd te zijn of is niet in PATH.
    echo Voor het volledig systeem met Grafana heeft u Docker nodig. 
    echo Download Docker Desktop van https://www.docker.com/products/docker-desktop/
    echo.
    echo Wilt u toch doorgaan met de installatie? (Druk op N om te stoppen)
    choice /c YN
    if %errorlevel% equ 2 (
        echo Installatie geannuleerd.
        pause
        exit /b 1
    )
)

echo Vereiste Python-packages installeren...
pip install requests influxdb pyyaml

echo.
echo Python-packages geinstalleerd.
echo.

REM Maak data directory
if not exist youless_data mkdir youless_data
echo Map 'youless_data' aangemaakt voor tijdelijke data.

echo.
echo ========================================
echo Installatiegids voor Youless Monitoring
echo ========================================
echo.
echo 1. Start het Docker-systeem (als Docker geinstalleerd is):
echo    docker-compose up -d
echo.
echo 2. Start de Youless-collector:
echo    python youless_to_influxdb.py
echo.
echo 3. Open Grafana in uw browser:
echo    http://localhost:3000
echo.
echo    Standaard inloggegevens:
echo    Gebruikersnaam: admin
echo    Wachtwoord: admin
echo.
echo ========================================
echo.
echo Configureer uw Youless-apparaten in config.yaml
echo.
pause