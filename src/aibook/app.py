from flask import Flask, render_template, send_from_directory, abort, send_file, request, jsonify
from pathlib import Path
import markdown
import os
import logging
import io
from weasyprint import HTML, CSS
import requests
import json
import re

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Directory configuratie
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / 'content' / 'chapters'
BUILD_DIR = BASE_DIR / 'build'
STATIC_DIR = BASE_DIR / 'static'
TEMPLATES_DIR = BASE_DIR / 'templates'

def setup_directories():
    """Zorg ervoor dat alle benodigde directories bestaan"""
    for directory in [CONTENT_DIR, BUILD_DIR, STATIC_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory {directory} is beschikbaar")

@app.route('/')
def index():
    """Render de hoofdpagina met een lijst van alle hoofdstukken"""
    chapters = []
    
    # Zoek alle markdown bestanden
    if CONTENT_DIR.exists():
        for file in sorted(CONTENT_DIR.glob('*.md')):
            chapter_name = file.stem
            nummer = chapter_name.split('_')[0]
            # Titel zonder nummer en spatie aan het begin
            titel_gestript = re.sub(r'^\d+[_\s.]*', '', chapter_name).replace('_', ' ').title()
            chapters.append({
                'filename': file.name,
                'name': titel_gestript,
                'nummer': nummer
            })
        logger.info(f"Gevonden hoofdstukken: {[c['name'] for c in chapters]}")
    
    # Bepaal het eerste hoofdstuk als next_chapter
    next_chapter = chapters[0]['filename'].replace('.md', '') if chapters else None
    
    return render_template('base.html',
                         title='AI voor Beginners',
                         chapters=chapters,
                         next_chapter=next_chapter)

@app.route('/<path:chapter_name>')
def show_chapter(chapter_name):
    """Render een specifiek hoofdstuk"""
    # Verwijder eventuele 'chapter/' prefix uit de URL
    chapter_name = chapter_name.split('/')[-1]
    # Voeg .md toe als het er niet is
    if not chapter_name.endswith('.md'):
        chapter_name += '.md'
    chapter_path = CONTENT_DIR / chapter_name
    logger.info(f"Probeer hoofdstuk te laden: {chapter_path}")
    if not chapter_path.exists():
        logger.warning(f"Hoofdstuk niet gevonden: {chapter_path}")
        abort(404)
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Converteer markdown naar HTML
    html_content = markdown.markdown(
        content,
        extensions=['extra', 'nl2br', 'sane_lists']
    )
    # Navigatie bepalen
    all_chapters = sorted(CONTENT_DIR.glob('*.md'))
    current_idx = [i for i, c in enumerate(all_chapters) if c.name == chapter_name]
    prev_chapter = next_chapter = None
    if current_idx:
        idx = current_idx[0]
        if idx > 0:
            prev_chapter = all_chapters[idx-1].stem
        if idx < len(all_chapters)-1:
            next_chapter = all_chapters[idx+1].stem
    chapters = []
    for file in all_chapters:
        chapters.append({
            'filename': file.name,
            'name': file.stem.replace('_', ' ').title()
        })
    return render_template('base.html',
                         title=chapter_name.replace('_', ' ').title().replace('.Md', ''),
                         content=html_content,
                         prev_chapter=prev_chapter,
                         next_chapter=next_chapter,
                         chapters=chapters)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve statische bestanden"""
    logger.info(f"Server statisch bestand: {filename}")
    return send_from_directory(STATIC_DIR, filename)

@app.route('/download_pdf/<chapter_name>')
def download_pdf(chapter_name):
    """Download een hoofdstuk als PDF"""
    if not chapter_name.endswith('.md'):
        chapter_name += '.md'
    chapter_path = CONTENT_DIR / chapter_name
    if not chapter_path.exists():
        abort(404)
    with open(chapter_path, 'r', encoding='utf-8') as f:
        content = f.read()
    html_content = markdown.markdown(
        content,
        extensions=['extra', 'nl2br', 'sane_lists']
    )
    # Simpele HTML wrapper voor PDF
    html = f"""
    <html><head><meta charset='utf-8'><style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 2cm; }}
    h1, h2, h3 {{ color: #2b3894; }}
    </style></head><body>
    <h1>{chapter_name.replace('_', ' ').replace('.md', '').title()}</h1>
    {html_content}
    </body></html>
    """
    pdf = HTML(string=html, base_url=str(BASE_DIR.resolve())).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 2cm; }')])
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{chapter_name.replace('.md', '')}.pdf"
    )

@app.route('/download_pdf/boek')
def download_entire_book():
    """Download het hele boek als PDF"""
    all_chapters = sorted(CONTENT_DIR.glob('*.md'))
    combined_content = ""
    
    for chapter in all_chapters:
        with open(chapter, 'r', encoding='utf-8') as f:
            content = f.read()
            chapter_title = chapter.stem.replace('_', ' ').title()
            combined_content += f"\n\n# {chapter_title}\n\n{content}"
    
    # Converteer markdown naar HTML
    html_content = markdown.markdown(
        combined_content,
        extensions=['extra', 'nl2br', 'sane_lists']
    )
    
    # Render de HTML met de template
    rendered_html = render_template(
        'pdf_template.html',
        title="AI Boek - Compleet",
        content=html_content
    )
    
    # Genereer PDF
    html = HTML(string=rendered_html)
    css = CSS(string='''
        @page {
            margin: 2cm;
            @top-right {
                content: counter(page);
            }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 0 1cm;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 1.5cm;
        }
        img {
            max-width: 100%;
            height: auto;
        }
    ''')
    
    pdf = html.write_pdf(stylesheets=[css])
    
    # Stuur de PDF als download
    return send_file(
        io.BytesIO(pdf),
        mimetype='application/pdf',
        as_attachment=True,
        download_name="AI_Boek_Compleet.pdf"
    )

@app.route('/ai_opdracht', methods=['POST'])
def ai_opdracht():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'Geen prompt ontvangen.'}), 400
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )
        antwoord = ''
        for line in response.iter_lines():
            if line:
                try:
                    chunk = line.decode('utf-8')
                    data = json.loads(chunk)
                    antwoord += data.get('response', '')
                except Exception as e:
                    continue
        return jsonify({'antwoord': antwoord.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    """Toon een vriendelijke 404 pagina"""
    logger.warning(f"404 error: {e}")
    return render_template('base.html',
                         title='Pagina Niet Gevonden',
                         content='<h1>😕 Oeps! Deze pagina bestaat niet.</h1>'), 404

if __name__ == '__main__':
    setup_directories()
    port = int(os.environ.get('PORT', 8002))
    logger.info(f"Server start op http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False) 