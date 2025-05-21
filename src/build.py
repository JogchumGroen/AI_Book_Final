import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
import yaml
import re

class BookBuilder:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.content_dir = os.path.join(self.base_dir, 'src', 'content', 'chapters')
        self.template_dir = os.path.join(self.base_dir, 'templates')
        self.static_dir = os.path.join(self.base_dir, 'static')
        self.build_dir = os.path.join(self.base_dir, 'build')
        
        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.template = self.env.get_template('base.html')
        
        # Setup markdown
        self.md = markdown.Markdown(extensions=['extra', 'codehilite'])
    
    def clean_build_dir(self):
        """Verwijder de build directory en maak deze opnieuw aan"""
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)
    
    def copy_static_files(self):
        """Kopieer statische bestanden naar de build directory"""
        static_dest = os.path.join(self.build_dir, 'static')
        shutil.copytree(self.static_dir, static_dest)
    
    def strip_first_h1(self, content):
        """Verwijder de eerste markdown H1 kopregel uit de content."""
        lines = content.splitlines()
        new_lines = []
        h1_found = False
        for line in lines:
            if not h1_found and line.strip().startswith('# '):
                h1_found = True
                continue  # sla deze regel over
            new_lines.append(line)
        return '\n'.join(new_lines)
    
    def process_markdown(self, file_path):
        """Verwerk een markdown bestand naar HTML"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraheer metadata (indien aanwezig)
        if content.startswith('---'):
            _, metadata, content = content.split('---', 2)
            metadata = yaml.safe_load(metadata)
        else:
            metadata = {}
        
        # Converteer markdown naar HTML
        html_content = self.md.convert(content)
        
        # Gebruik de template
        html = self.template.render(
            title=metadata.get('title', 'AI Boek'),
            content=html_content
        )
        
        return html
    
    def get_chapter_list(self):
        """Maak een gesorteerde en genummerde lijst van hoofdstukken (nummer, filename, name)"""
        chapters = []
        print(f"[DEBUG] Inhoud van content_dir ({self.content_dir}): {os.listdir(self.content_dir)}")
        for idx, file in enumerate(sorted(os.listdir(self.content_dir)), 1):
            if file.endswith('.md'):
                path = os.path.join(self.content_dir, file)
                print(f"[DEBUG] Verwerk bestand: {path}")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Probeer titel uit YAML frontmatter te halen, anders uit eerste kop
                title = None
                if content.startswith('---'):
                    _, metadata, _ = content.split('---', 2)
                    meta = yaml.safe_load(metadata)
                    title = meta.get('title') if meta else None
                if not title:
                    m = re.search(r'^# (.+)$', content, re.MULTILINE)
                    if m:
                        title = m.group(1)
                if not title:
                    title = file.replace('.md', '')
                chapters.append({
                    'nummer': idx,
                    'filename': file.replace('.md', '.html'),
                    'name': title
                })
        print(f"[DEBUG] Gemaakte hoofdstukkenlijst: {chapters}")
        return chapters

    def build(self):
        print("Start bouwen van het boek...")
        self.clean_build_dir()
        self.copy_static_files()
        chapters = self.get_chapter_list()
        chapter_files = [c['filename'] for c in chapters]
        for idx, chapter in enumerate(chapters):
            md_path = os.path.join(self.content_dir, chapter['filename'].replace('.html', '.md'))
            print(f"[DEBUG] Probeer te verwerken: {md_path}")
            if not os.path.exists(md_path):
                print(f"[DEBUG] Bestand bestaat niet: {md_path}")
                continue
            rel_path = '.'
            html_path = self.build_dir
            prev_chapter = chapter_files[idx-1] if idx > 0 else None
            next_chapter = chapter_files[idx+1] if idx < len(chapter_files)-1 else None
            with open(md_path, encoding='utf-8') as f:
                raw_content = f.read()
            content_no_h1 = self.strip_first_h1(raw_content)
            html_rendered = self.template.render(
                title=chapter['name'],
                content=markdown.markdown(content_no_h1, extensions=['extra', 'codehilite']),
                chapters=chapters,
                prev_chapter=prev_chapter,
                next_chapter=next_chapter
            )
            html_file = os.path.join(html_path, chapter['filename'])
            print(f"[DEBUG] Schrijf naar: {html_file}")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_rendered)
            # Maak van 00_inhoudsopgave.md ook index.html
            if chapter['filename'] == '00_inhoudsopgave.html':
                index_html_path = os.path.join(self.build_dir, 'index.html')
                print(f"[DEBUG] Schrijf ook naar: {index_html_path}")
                with open(index_html_path, 'w', encoding='utf-8') as f:
                    f.write(html_rendered)
        print("Klaar! Het boek is gebouwd in de build directory.")

if __name__ == '__main__':
    builder = BookBuilder()
    builder.build() 