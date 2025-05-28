#!/bin/bash

# Kleuren voor logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging functies
log() {
    echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +%H:%M:%S)]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +%H:%M:%S)] Fout:${NC} $1"
    exit 1
}

# Bepaal het pad naar dit script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ga naar de project directory
cd "$SCRIPT_DIR" || error "Kon niet naar project directory gaan"

# Check of we in de juiste directory zijn
if [ ! -f "app.py" ]; then
    error "Script moet worden uitgevoerd vanuit de AI_Book directory (app.py niet gevonden)"
fi

# Controleer of Python beschikbaar is
if ! command -v python3 &> /dev/null; then
    error "Python3 is niet geïnstalleerd"
fi

# Controleer of virtualenv bestaat, zo niet maak het aan
if [ ! -d "venv" ]; then
    error "Virtuele omgeving niet gevonden. Maak deze aan met: python3 -m venv venv"
fi

# Activeer virtualenv
source venv/bin/activate || error "Kon virtuele omgeving niet activeren"

# Laad .env variabelen vóór het starten van de server
if [ -f .env ]; then
    log "Laad .env variabelen..."
    export $(grep -v '^#' .env | xargs)
fi

# Stel FLASK_ENV in
export FLASK_ENV=development

# Stop bestaande server op poort 8000
if lsof -i:8000 > /dev/null; then
    warn "Er draait al een proces op poort 8000. Dit wordt nu gestopt..."
    kill $(lsof -t -i:8000) || error "Kon proces op poort 8000 niet stoppen"
    sleep 2
fi

log "Starten van de server op de voorgrond (druk Ctrl+C om te stoppen)..."
python3 app.py 