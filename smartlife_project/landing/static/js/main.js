// Hero Section Module
const HeroSection = (function() {
    let currentSlide = 0;
    let isTransitioning = false;
    let autoAdvanceTimer = null;
    const TRANSITION_DURATION = 500; // ms
    const AUTO_ADVANCE_INTERVAL = 5000; // ms

    function init() {
        const heroItems = document.querySelectorAll('.hero-item');
        const navDots = document.querySelectorAll('.hero-nav-dot');

        if (heroItems.length === 0) {
            console.log('No hero items found, hero section initialization skipped');
            return;
        }

        // Initialize first slide
        if (heroItems.length > 0) {
            heroItems[0].classList.add('active');
        }
        
        // Initialize background images
        initializeBackgrounds(heroItems);
        
        // Set up navigation if nav dots exist
        if (navDots.length > 0) {
            setupNavigation(navDots);
            navDots[0].classList.add('active');
        }
        
        // Start auto-advancing slides if more than one slide
        if (heroItems.length > 1) {
            startAutoAdvance(heroItems);
        }
    }

    function initializeBackgrounds(items) {
        items.forEach(item => {
            const backgroundImage = item.getAttribute('data-background');
            if (backgroundImage) {
                // Set background image
                item.style.backgroundImage = `url('${backgroundImage}')`;
                item.style.backgroundSize = 'cover';
                item.style.backgroundPosition = 'center';
                item.style.backgroundRepeat = 'no-repeat';
            } else {
                // Add a default background gradient
                item.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }
        });
    }

    function setupNavigation(dots) {
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                if (!isTransitioning) {
                    // Reset auto-advance timer when manually navigating
                    if (autoAdvanceTimer) {
                        clearInterval(autoAdvanceTimer);
                    }
                    goToSlide(index);
                    startAutoAdvance(document.querySelectorAll('.hero-item'));
                }
            });
        });
    }

    function startAutoAdvance(items) {
        // Clear any existing timer
        if (autoAdvanceTimer) {
            clearInterval(autoAdvanceTimer);
        }
        
        // Set new timer
        autoAdvanceTimer = setInterval(() => {
            const nextSlide = (currentSlide + 1) % items.length;
            goToSlide(nextSlide);
        }, AUTO_ADVANCE_INTERVAL);
    }

    function goToSlide(index) {
        if (isTransitioning || index === currentSlide) return;
        
        isTransitioning = true;
        
        const heroItems = document.querySelectorAll('.hero-item');
        const navDots = document.querySelectorAll('.hero-nav-dot');
        
        // Fade out current slide
        heroItems[currentSlide].classList.remove('active');
        
        // Show next slide
        heroItems[index].classList.add('active');
        
        // Update navigation dots if they exist
        if (navDots.length > 0) {
            navDots[currentSlide].classList.remove('active');
            navDots[index].classList.add('active');
        }
        
        currentSlide = index;
        
        // Reset transition flag after animation
        setTimeout(() => {
            isTransitioning = false;
        }, TRANSITION_DURATION);
    }

    return {
        init: init
    };
})();

// Form validation
const FormValidation = (function() {
    function init() {
        // Enable Bootstrap form validation
        const forms = document.querySelectorAll('.needs-validation');
        
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }
    
    return {
        init: init
    };
})();

// Initialize all modules when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    HeroSection.init();
    FormValidation.init();
});
