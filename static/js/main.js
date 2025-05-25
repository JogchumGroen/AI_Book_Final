document.addEventListener('DOMContentLoaded', () => {
    // Highlight huidige pagina in navigatie
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.backgroundColor = '#e0e0e0';
        }
    });

    // Zoek het AI voorbeeld in de content
    const aiVoorbeeld = document.querySelector('.ai-voorbeeld');
    if (aiVoorbeeld) {
        document.getElementById('ai-voorbeeld-tekst').textContent = aiVoorbeeld.textContent.trim();
        aiVoorbeeld.style.display = 'none'; // Verberg het originele element
    }
}); 