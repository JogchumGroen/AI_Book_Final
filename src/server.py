from flask import Flask, send_from_directory, redirect
import os

app = Flask(__name__)

# Bepaal het pad naar de build directory
build_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'build')

@app.route('/')
def index():
    """Redirect naar de inhoudsopgave"""
    return redirect('/chapters/00_inhoudsopgave.html')

@app.route('/chapters/<path:filename>')
def serve_chapter(filename):
    """Serveer hoofdstukken"""
    return send_from_directory(os.path.join(build_dir, 'chapters'), filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serveer statische bestanden (CSS, JS, afbeeldingen)"""
    return send_from_directory(os.path.join(build_dir, 'static'), filename)

if __name__ == '__main__':
    # Controleer of de build directory bestaat
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
        print(f"Build directory aangemaakt: {build_dir}")
    
    print(f"Server start op http://localhost:8000")
    app.run(host='localhost', port=8000, debug=True) 