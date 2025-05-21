// Functie om de navigatie responsive te maken
function setupNavigation() {
    const nav = document.querySelector('nav');
    const navLinks = document.querySelector('.nav-links');
    
    // Voeg een menu knop toe voor mobiele weergave
    const menuButton = document.createElement('button');
    menuButton.className = 'menu-button';
    menuButton.innerHTML = '☰';
    nav.insertBefore(menuButton, navLinks);
    
    // Toggle menu bij klik
    menuButton.addEventListener('click', () => {
        navLinks.classList.toggle('show');
    });
}

// Functie om code snippets te highlighten
function setupCodeHighlighting() {
    const codeBlocks = document.querySelectorAll('pre code');
    if (codeBlocks.length > 0) {
        // Hier kunnen we later een syntax highlighting library toevoegen
        codeBlocks.forEach(block => {
            block.classList.add('code-block');
        });
    }
}

// Functie om afbeeldingen te vergroten bij klik
function setupImageZoom() {
    const images = document.querySelectorAll('article img');
    images.forEach(img => {
        img.addEventListener('click', () => {
            img.classList.toggle('zoomed');
        });
    });
}

// Initialiseer alle functies wanneer de DOM geladen is
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupCodeHighlighting();
    setupImageZoom();
}); 