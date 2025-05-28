# AI Boek Server

Een Flask-gebaseerde server voor het AI Boek project. Dit project bevat alle hoofdstukken in markdown, een moderne webinterface en automatische backups.

## Verbinding met GitHub

Dit project is gekoppeld aan een GitHub repository: [AI_Book_Final](https://github.com/JogchumGroen/AI_Book_Final).

- Alle code, hoofdstukken en wijzigingen worden via deze repository beheerd.
- Gebruik altijd `git add`, `git commit` en `git push` om je wijzigingen te bewaren en te synchroniseren met GitHub.
- Voor samenwerking of backup is GitHub de centrale plek.

**Let op:**
Elke keer dat je mij (de AI-assistent) vraagt naar de README, gebruik ik deze als dé referentie voor de structuur, workflow en afspraken van het project. Verwijs dus gerust naar deze README als je wilt dat ik weet hoe het project werkt of is opgebouwd.

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
   source venv/bin/activate
   FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 python3 -m flask run --port=8002
   ```
   De server draait standaard op [http://localhost:8002](http://localhost:8002)

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
- De server herlaadt automatisch bij wijzigingen (debug mode is ingeschakeld)
- Backups kun je handmatig maken (zie onder)

## Probleemoplossing

1. **Server start niet**
   - Controleer of poort 8002 vrij is
   - Stop handmatig andere processen op poort 8002 indien nodig
   - Zorg ervoor dat je in de virtuele omgeving bent (`source venv/bin/activate`)

2. **Afbeeldingen niet zichtbaar**
   - Controleer of de afbeelding in `static/images/` staat

3. **Debug Mode**
   - Debug mode is standaard ingeschakeld
   - Debugger PIN: 371-449-073 (indien nodig voor debugging)

## Licentie

MIT License

## Backup maken

Maak een backup van het hele project met:

    tar -czf backup_ai_voor_beginners_$(date +%Y%m%d_%H%M%S).tar.gz .

De backup wordt opgeslagen in de hoofdmap. Oude backups kun je veilig verwijderen uit de map `RECOVERY/`.

## Lokale server starten

Volg deze stappen om de server lokaal te draaien:

1. **Maak (eenmalig) een virtuele omgeving aan:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
   Dit zorgt ervoor dat alle benodigde Python-pakketten lokaal worden geïnstalleerd, zonder je systeem te vervuilen.

2. **Activeer de virtuele omgeving (elke keer als je aan het project werkt):**
   ```bash
   source venv/bin/activate
   ```

3. **Start de server:**
   ```bash
   python3 app.py
   ```
   Of, als je een specifieke poort wilt gebruiken (bijvoorbeeld 8002):
   ```bash
   FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 python3 -m flask run --port=8002
   ```

4. **Open je browser en ga naar:**
   [http://localhost:8001](http://localhost:8001) (of de poort die je gekozen hebt)

### Veelvoorkomende problemen
- **ModuleNotFoundError: No module named 'flask'**
  > Je zit waarschijnlijk niet in de virtuele omgeving. Voer eerst `source venv/bin/activate` uit.
- **Port 8001 is in use**
  > Er draait al iets op deze poort. Kies een andere poort of stop het andere proces.
- **requirements.txt ontbreekt of is niet up-to-date**
  > Vraag om het juiste bestand of update met `pip install -r requirements.txt`.

---

*Laatste update: mei 2025 – projectstructuur en workflow volledig vernieuwd en vereenvoudigd.*

## Let op bij uploaden naar GIT

Backup-bestanden (zoals .tar.gz, .bak en de map RECOVERY/) worden nu genegeerd door GIT. Upload deze dus niet naar de repository, maar bewaar ze alleen lokaal voor eigen gebruik.
