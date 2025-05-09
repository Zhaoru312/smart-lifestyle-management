// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Get all forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Hero section functionality
document.addEventListener('DOMContentLoaded', function() {
    const heroItems = document.querySelectorAll('.hero-item');
    const navDots = document.querySelectorAll('.hero-nav-dot');
    let currentSlide = 0;
    let isTransitioning = false;

    // Initialize background images
    heroItems.forEach(item => {
        const backgroundImage = item.getAttribute('data-background');
        if (backgroundImage) {
            // Set background image using CSS variable
            item.style.setProperty('--background-image', `url('${backgroundImage}')`);
            // Also set it directly for better compatibility
            item.style.backgroundImage = `url('${backgroundImage}')`;
        } else {
            // Add a default background gradient
            item.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
    });

    // Auto-advance slides every 5 seconds
    setInterval(advanceSlide, 5000);

    // Click handler for navigation dots
    navDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            if (!isTransitioning) {
                goToSlide(index);
            }
        });
    });

    function goToSlide(index) {
        if (isTransitioning || index === currentSlide) return;
        
        isTransitioning = true;
        
        // Fade out current slide
        heroItems[currentSlide].classList.add('d-none');
        
        // Show next slide
        heroItems[index].classList.remove('d-none');
        
        // Update navigation dots
        navDots[currentSlide].classList.remove('active');
        navDots[index].classList.add('active');
        
        currentSlide = index;
        
        // Reset transition flag after animation
        setTimeout(() => {
            isTransitioning = false;
        }, 500);
    }

    function advanceSlide() {
        const nextSlide = (currentSlide + 1) % heroItems.length;
        goToSlide(nextSlide);
    }
});
