#!/bin/bash

# Activeer virtuele omgeving indien aanwezig
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start de Flask server met automatische herstart bij wijzigingen
watchmedo auto-restart --patterns="*.py;*.md;*.html;*.css;*.js" --recursive -- python3 app.py 