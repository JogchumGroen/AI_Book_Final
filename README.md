# AI Boek Server

Een Flask-gebaseerde server voor het AI Boek project, inclusief lokale AI via Ollama en automatische backups.

## Repository en Workflow

Dit project is gehost op GitHub: https://github.com/JogchumGroen/AI_Book

### Belangrijke mappen
- `AI_Book/` - De hoofdmap van het project
  - `src/content/chapters/` - Markdown hoofdstukken
  - `templates/` - HTML templates
  - `static/` - Statische bestanden
  - `backup/` - Automatische backups

### Workflow
- Alle wijzigingen worden direct in de AI_Book directory gemaakt
- Gebruik `git add`, `git commit` en `git push` vanuit de AI_Book directory
- De server wordt gestart met `./start_ai_book.sh` vanuit de AI_Book directory

## Vereisten

- Python 3.8 of hoger
- Cairo graphics library (voor SVG conversie)
- Ollama (voor lokale AI, met het model `mistral`)

### Cairo Installatie

#### macOS
```bash
brew install cairo
```

#### Ubuntu/Debian
```bash
sudo apt-get install libcairo2-dev
```

### Ollama Installatie

Zie: https://ollama.com/download  
Na installatie:  
```bash
ollama serve &
ollama pull mistral
```

## Installatie en starten

1. Maak een virtuele omgeving aan (eenmalig):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start de server met:
   ```bash
   ./start_ai_book.sh
   ```
   Dit script:
   - Stopt automatisch oude servers op poort 8000
   - Start Ollama (indien nodig) en download het model `mistral` als dat nog niet aanwezig is
   - Start de boekserver op http://localhost:8000

3. Open [http://localhost:8000](http://localhost:8000) in je browser.

## Project Structuur

```
AI_Book/
├── app.py                # Flask applicatie
├── start_ai_book.sh      # Startup script (gebruiken!)
├── src/
│   ├── content/
│   │   └── chapters/     # Markdown hoofdstukken
│   ├── static/           # Statische bestanden (afbeeldingen, css, js)
│   └── templates/        # HTML templates
├── static/
│   └── images/           # Afbeeldingen
├── templates/            # HTML templates
├── build/                # Gebouwde bestanden
├── backup/               # Automatische backups
└── ...                   # Overige scripts en config
```

## Ontwikkeling

- Plaats nieuwe hoofdstukken in `src/content/chapters/`
- Plaats afbeeldingen in `static/images/`
- De server herlaadt automatisch bij wijzigingen (tenzij debug mode uit staat)
- Backups worden automatisch gemaakt en oude worden opgeschoond

## Probleemoplossing

1. **Server start niet**
   - Controleer of poort 8000 vrij is (het script stopt automatisch als de poort bezet blijft)
   - Stop handmatig andere processen op poort 8000 indien nodig

2. **AI-bot werkt niet**
   - Controleer of Ollama draait (`ollama serve`)
   - Controleer of het model `mistral` is gedownload (`ollama list`)
   - Zie de log `/tmp/ollama.log` voor foutmeldingen

3. **Afbeeldingen niet zichtbaar**
   - Controleer of Cairo is geïnstalleerd
   - Voer `convert_images.py` handmatig uit

## Licentie

MIT License

## Lokale AI via Ollama (Mistral)

- Je kunt AI-opdrachten uitvoeren zonder kosten of limieten, volledig lokaal.
- Het script zorgt automatisch dat Ollama draait en het model `mistral` beschikbaar is.

## Backup
- Alle belangrijke bestanden en mappen worden automatisch geback-upt in de map `backup/`.
- Oude backups worden automatisch verwijderd voor overzicht.
- Zie ook `README_BACKUP_HISTORY.md` voor een overzicht van de projectgeschiedenis.

## PDF-download

- Je kunt elk hoofdstuk als PDF downloaden via de knop op de hoofdstukpagina.
- Op de inhoudsopgave-pagina kun je nu ook in één keer alle hoofdstukken als één PDF downloaden via de grote knop onderaan.

## Wijzigingen sinds livegang (mei 2025)

- Navigatie-menu (Hoofdstukken) voorzien van nette nummering.
- Dubbele titels bovenaan hoofdstukken verwijderd (eerste H1 uit markdown wordt niet meer getoond).
- Hoofdstuktitels in het menu en op de pagina zijn nu overal zonder nummer, voor consistentie.
- Navigatie Vorige/Volgende werkt nu ook in de statische site.
- Kleine verbeteringen aan de opmaak en structuur van hoofdstukken.
- Build-script uitgebreid met debug en automatische correctie van titels.

> Volgende keer kun je hierop verder bouwen, bijvoorbeeld door meer interactieve elementen toe te voegen of de AI-opdracht-blok te verbeteren.

## Backup maken

Maak een backup van het hele project met:

    tar -czf backup_ai_voor_beginners_$(date +%Y%m%d_%H%M%S).tar.gz .

De backup wordt opgeslagen in de hoofdmap. Oude backups kun je veilig verwijderen uit de map `backup/`.
