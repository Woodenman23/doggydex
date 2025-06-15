// DoggyDex JavaScript
console.log('DoggyDex loaded successfully');

// Initialize any interactive features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for internal links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add fade-in animation class to main containers
    const containers = document.querySelectorAll('.main-container, .results-container');
    containers.forEach(container => {
        container.classList.add('fade-in');
    });
});