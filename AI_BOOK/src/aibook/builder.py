"""
Book Builder module.

Verantwoordelijk voor het omzetten van markdown content naar HTML.
"""

import os
import shutil
import logging
from pathlib import Path
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

class BookBuilder:
    """Bouwt het boek van markdown naar HTML."""
    
    def __init__(self, output_dir='dist'):
        self.base_dir = Path.cwd()
        self.content_dir = self.base_dir / 'src' / 'content' / 'chapters'
        self.output_dir = Path(output_dir)
        self.assets_dir = self.base_dir / 'static'
        
        # Setup Jinja2
        templates_dir = self.base_dir / 'aibook' / 'templates'
        self.jinja_env = Environment(loader=FileSystemLoader(str(templates_dir)))
        
        # Setup Markdown
        self.md = markdown.Markdown(extensions=['extra', 'meta', 'codehilite'])
    
    def clean_output_dir(self):
        """Maak de output directory leeg."""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
    
    def copy_assets(self):
        """Kopieer alle assets naar de output directory."""
        if self.assets_dir.exists():
            dest = self.output_dir / 'assets'
            shutil.copytree(self.assets_dir, dest, dirs_exist_ok=True)
    
    def process_markdown(self, file_path: Path) -> dict:
        """Verwerk een markdown bestand naar HTML."""
        post = frontmatter.load(file_path)
        html_content = self.md.convert(post.content)
        
        return {
            'content': html_content,
            'metadata': post.metadata,
            'title': post.metadata.get('title', 'Untitled')
        }
    
    def build_chapter(self, file_path: Path):
        """Bouw een enkel hoofdstuk."""
        logger.info(f"Verwerk hoofdstuk: {file_path.name}")
        
        # Verwerk de content
        processed = self.process_markdown(file_path)
        
        # Laad de template
        template = self.jinja_env.get_template('chapter.html')
        
        # Render de HTML
        html = template.render(**processed)
        
        # Bepaal het output pad
        rel_path = file_path.relative_to(self.content_dir)
        output_path = self.output_dir / rel_path.with_suffix('.html')
        
        # Maak de output directory als deze niet bestaat
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Schrijf het bestand
        output_path.write_text(html)
    
    def build(self):
        """Bouw het complete boek."""
        logger.info("Start bouwen van het boek...")
        
        # Voorbereiden
        self.clean_output_dir()
        self.copy_assets()
        
        # Verwerk alle markdown bestanden
        chapters_dir = self.content_dir
        if not chapters_dir.exists():
            raise FileNotFoundError(f"Chapters directory niet gevonden: {chapters_dir}")
        
        # Sorteer de hoofdstukken op naam
        md_files = sorted(list(chapters_dir.glob('*.md')))
        
        for idx, md_file in enumerate(md_files):
            prev_chapter = md_files[idx-1] if idx > 0 else None
            next_chapter = md_files[idx+1] if idx < len(md_files)-1 else None

            # Verwerk de content
            processed = self.process_markdown(md_file)
            
            # Voeg navigatie toe
            processed['prev_chapter'] = prev_chapter.with_suffix('.html').name if prev_chapter else None
            processed['next_chapter'] = next_chapter.with_suffix('.html').name if next_chapter else None

            # Laad de template
            template = self.jinja_env.get_template('chapter.html')
            html = template.render(**processed)
            
            # Bepaal het output pad
            rel_path = md_file.relative_to(self.content_dir)
            output_path = self.output_dir / rel_path.with_suffix('.html')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html)
        
        logger.info(f"Boek succesvol gebouwd in: {self.output_dir}") 