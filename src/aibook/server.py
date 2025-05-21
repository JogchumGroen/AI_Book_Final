"""
Book Server module.

Verantwoordelijk voor het serveren van het gebouwde boek via een ontwikkelserver.
"""

from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__, 
           template_folder=str(Path(__file__).parent.parent / 'templates'),
           static_folder=str(Path(__file__).parent.parent / 'static'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("\nServer wordt gestart op http://localhost:8000")
    app.run(host='localhost', port=8000, debug=True) 