document.addEventListener('DOMContentLoaded', function() {
    var dropbtn = document.querySelector('.dropbtn');
    var dropdown = document.querySelector('.dropdown-content');
    if(dropbtn && dropdown) {
        dropbtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';
        });
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target) && e.target !== dropbtn) {
                dropdown.style.display = 'none';
            }
        });
    }
}); 