# AI Boek Server

Een Flask-gebaseerde server voor het AI Boek project. Dit project bevat alle hoofdstukken in markdown, een moderne webinterface en automatische backups.

## Repository en Workflow

Dit project is gehost op GitHub: https://github.com/JogchumGroen/AI_Book_Final

### Belangrijke mappen
- `src/content/chapters/` - Markdown hoofdstukken
- `templates/` - HTML templates
- `static/` - Statische bestanden (afbeeldingen, css, js)
- `build/` - Gebouwde bestanden (optioneel)
- `RECOVERY/` - (Lokaal) backups en oude versies

### Workflow
- Alle wijzigingen worden direct in de root van het project gemaakt
- Gebruik `git add`, `git commit` en `git push` vanuit de root
- De server wordt gestart met `./start.sh` of handmatig met `python3 app.py`

## Vereisten

- Python 3.8 of hoger

## Installatie en starten

1. Maak een virtuele omgeving aan (eenmalig):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start de server met:
   ```bash
   ./start.sh
   ```
   of handmatig:
   ```bash
   source venv/bin/activate
   python3 app.py
   ```
   De server draait standaard op [http://localhost:8001](http://localhost:8001)

## Project Structuur

```
├── app.py                # Flask applicatie
├── start.sh              # Startup script
├── src/
│   ├── content/
│   │   └── chapters/     # Markdown hoofdstukken
│   ├── static/           # (optioneel) extra statische bestanden
│   └── templates/        # (optioneel) extra templates
├── static/
│   ├── css/              # Stijlen
│   ├── js/               # JavaScript
│   └── images/           # Afbeeldingen
├── templates/            # HTML templates
├── build/                # Gebouwde bestanden
├── RECOVERY/             # (Lokaal) backups en oude versies
├── requirements.txt      # Python dependencies
├── render.yaml           # Render.com configuratie
├── .gitignore            # Git ignore file
└── ...                   # Overige scripts en config
```

## Ontwikkeling

- Plaats nieuwe hoofdstukken in `src/content/chapters/`
- Plaats afbeeldingen in `static/images/`
- De server herlaadt automatisch bij wijzigingen (tenzij debug mode uit staat)
- Backups kun je handmatig maken (zie onder)

## Probleemoplossing

1. **Server start niet**
   - Controleer of poort 8001 vrij is
   - Stop handmatig andere processen op poort 8001 indien nodig

2. **Afbeeldingen niet zichtbaar**
   - Controleer of de afbeelding in `static/images/` staat

## Licentie

MIT License

## Backup maken

Maak een backup van het hele project met:

    tar -czf backup_ai_voor_beginners_$(date +%Y%m%d_%H%M%S).tar.gz .

De backup wordt opgeslagen in de hoofdmap. Oude backups kun je veilig verwijderen uit de map `RECOVERY/`.

---

*Laatste update: mei 2025 – projectstructuur en workflow volledig vernieuwd en vereenvoudigd.*
