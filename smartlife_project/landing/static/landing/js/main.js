/**
 * SmartLife Landing Page JavaScript
 * Enhances the user experience with interactive elements and form validation
 */

'use strict';

// Hero Section Module - Handles the hero slider functionality
const HeroSection = (function() {
    // Private variables
    let currentSlide = 0;
    let isTransitioning = false;
    let autoAdvanceTimer = null;
    let pauseOnHover = true;
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

// FAQ Section Module
const FAQSection = (function() {
    function init() {
        setupAccordion();
    }
    
    function setupAccordion() {
        const faqItems = document.querySelectorAll('.faq-item');
        
        faqItems.forEach(item => {
            const header = item.querySelector('.faq-header');
            const content = item.querySelector('.faq-content');
            
            if (header && content) {
                header.addEventListener('click', function() {
                    // Toggle active class
                    item.classList.toggle('active');
                    
                    // Toggle content visibility
                    if (item.classList.contains('active')) {
                        content.style.maxHeight = content.scrollHeight + 'px';
                    } else {
                        content.style.maxHeight = '0';
                    }
                });
            }
        });
    }
    
    return {
        init: init
    };
})();

// Form Validation Module
const FormValidation = (function() {
    function init() {
        initContactForm();
        initLoginForm();
        initRegisterForm();
        initPasswordReset();
    }
    
    function initContactForm() {
        const contactForm = document.querySelector('#contact-form');
        if (!contactForm) return;
        
        contactForm.addEventListener('submit', function(event) {
            if (!validateForm(contactForm)) {
                event.preventDefault();
            }
        });
    }
    
    function initLoginForm() {
        const loginForm = document.querySelector('#login-form');
        if (!loginForm) return;
        
        loginForm.addEventListener('submit', function(event) {
            if (!validateForm(loginForm)) {
                event.preventDefault();
            }
        });
    }
    
    function initRegisterForm() {
        const registerForm = document.querySelector('#register-form');
        if (!registerForm) return;
        
        // Password strength meter
        const passwordInput = registerForm.querySelector('input[name="password"]');
        if (passwordInput) {
            const strengthMeter = document.createElement('div');
            strengthMeter.className = 'password-strength mt-2';
            strengthMeter.innerHTML = '<div class="progress" style="height: 5px;"><div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div></div><small class="form-text mt-1">Password strength: <span>Weak</span></small>';
            
            passwordInput.parentNode.insertBefore(strengthMeter, passwordInput.nextSibling);
            
            passwordInput.addEventListener('input', function() {
                updatePasswordStrength(this.value, strengthMeter);
            });
        }
        
        // Password confirmation validation
        const confirm_passwordinput = registerForm.querySelector('input[name="confirm_password"]');
        if (confirm_passwordinput && passwordInput) {
            confirm_passwordinput.addEventListener('input', function() {
                if (this.value !== passwordInput.value) {
                    this.setCustomValidity('Passwords do not match');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        registerForm.addEventListener('submit', function(event) {
            if (!validateForm(registerForm)) {
                event.preventDefault();
            }
        });
    }
    
    function initPasswordReset() {
        const resetForm = document.querySelector('#password-reset-form');
        if (!resetForm) return;
        
        resetForm.addEventListener('submit', function(event) {
            if (!validateForm(resetForm)) {
                event.preventDefault();
            }
        });
    }
    
    function validateForm(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input:not([type="hidden"]), textarea, select');
        
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                isValid = false;
                showError(input);
            } else {
                clearError(input);
            }
            
            // Add input event listener to clear errors on typing
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    clearError(this);
                }
            });
        });
        
        return isValid;
    }
    
    function showError(input) {
        input.classList.add('is-invalid');
        
        // Create or update error message
        let errorElement = input.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains('invalid-feedback')) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            input.parentNode.insertBefore(errorElement, input.nextSibling);
        }
        
        errorElement.textContent = input.validationMessage || 'This field is required';
    }
    
    function clearError(input) {
        input.classList.remove('is-invalid');
        const errorElement = input.nextElementSibling;
        if (errorElement && errorElement.classList.contains('invalid-feedback')) {
            errorElement.textContent = '';
        }
    }
    
    function updatePasswordStrength(password, meterElement) {
        // Simple password strength algorithm
        let strength = 0;
        
        if (password.length >= 8) strength += 25;
        if (password.match(/[a-z]+/)) strength += 25;
        if (password.match(/[A-Z]+/)) strength += 25;
        if (password.match(/[0-9]+/)) strength += 25;
        if (password.match(/[^a-zA-Z0-9]+/)) strength += 25;
        
        // Cap at 100%
        strength = Math.min(100, strength);
        
        // Update UI
        const progressBar = meterElement.querySelector('.progress-bar');
        const strengthText = meterElement.querySelector('span');
        
        progressBar.style.width = strength + '%';
        progressBar.setAttribute('aria-valuenow', strength);
        
        // Set color based on strength
        if (strength < 30) {
            progressBar.className = 'progress-bar bg-danger';
            strengthText.textContent = 'Weak';
        } else if (strength < 70) {
            progressBar.className = 'progress-bar bg-warning';
            strengthText.textContent = 'Medium';
        } else {
            progressBar.className = 'progress-bar bg-success';
            strengthText.textContent = 'Strong';
        }
    }
    
    return {
        init: init
    };
})();

// Accessibility Enhancements Module
const Accessibility = (function() {
    function init() {
        enhanceFormLabels();
        setupKeyboardNavigation();
    }
    
    function enhanceFormLabels() {
        // Ensure all form inputs have associated labels
        const inputs = document.querySelectorAll('input:not([type="hidden"]), textarea, select');
        
        inputs.forEach(input => {
            // Skip if input already has a label
            if (input.id && document.querySelector(`label[for="${input.id}"]`)) {
                return;
            }
            
            // Create an ID if none exists
            if (!input.id) {
                input.id = 'input-' + Math.random().toString(36).substr(2, 9);
            }
            
            // Create a label if none exists
            if (!document.querySelector(`label[for="${input.id}"]`)) {
                const label = document.createElement('label');
                label.setAttribute('for', input.id);
                label.className = 'form-label';
                
                // Use placeholder or name as label text
                const labelText = input.placeholder || input.name || 'Input field';
                label.textContent = labelText.charAt(0).toUpperCase() + labelText.slice(1);
                
                // Insert label before input
                input.parentNode.insertBefore(label, input);
            }
        });
    }
    
    function setupKeyboardNavigation() {
        // Add focus styles for keyboard navigation
        const style = document.createElement('style');
        style.textContent = `
            a:focus, button:focus, input:focus, textarea:focus, select:focus {
                outline: 2px solid var(--primary-color) !important;
                outline-offset: 2px !important;
            }
        `;
        document.head.appendChild(style);
        
        // Add skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                }
            });
        }
    }
    
    return {
        init: init
    };
})();

// Animation Effects Module
const AnimationEffects = (function() {
    function init() {
        initScrollAnimations();
        initPageLoadAnimations();
    }
    
    function initPageLoadAnimations() {
        // Apply animations to hero section elements
        const heroTitle = document.querySelector('.hero-title');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroButton = document.querySelector('.hero-cta');
        
        if (heroTitle) {
            heroTitle.classList.add('slide-in-left');
        }
        
        if (heroSubtitle) {
            heroSubtitle.classList.add('fade-in', 'delay-200');
        }
        
        if (heroButton) {
            heroButton.classList.add('fade-in', 'delay-400');
        }
        
        // Apply animations to feature cards
        const featureCards = document.querySelectorAll('.feature-card');
        featureCards.forEach((card, index) => {
            card.classList.add('fade-in');
            card.classList.add(`delay-${(index + 1) * 100}`);
        });
        
        // Apply animations to testimonials
        const testimonials = document.querySelectorAll('.testimonial-card');
        testimonials.forEach((testimonial, index) => {
            testimonial.classList.add('fade-in');
            testimonial.classList.add(`delay-${(index + 1) * 100}`);
        });
    }
    
    function initScrollAnimations() {
        // Only run if IntersectionObserver is supported
        if (!('IntersectionObserver' in window)) return;
        
        const options = {
            root: null, // viewport
            rootMargin: '0px',
            threshold: 0.1 // 10% of the element visible
        };
        
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    
                    // Apply the animation class based on data attribute
                    const animationType = element.dataset.animation || 'fade-in';
                    element.classList.add(animationType);
                    
                    // Apply delay if specified
                    if (element.dataset.delay) {
                        element.classList.add(`delay-${element.dataset.delay}`);
                    }
                    
                    // Stop observing after animation is applied
                    observer.unobserve(element);
                }
            });
        }, options);
        
        // Observe elements with data-animate attribute
        document.querySelectorAll('[data-animate]').forEach(element => {
            observer.observe(element);
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
    
    // Initialize accessibility enhancements
    Accessibility.init();
    
    // Initialize animation effects
    AnimationEffects.init();
});

// Newsletter form handling
const newsletterForms = document.querySelectorAll('.newsletter-form');
if (newsletterForms.length > 0) {
    newsletterForms.forEach(form => {
        const emailInput = form.querySelector('input[type="email"]');
        if (!emailInput) return;

        // Clear errors on typing
        emailInput.addEventListener('input', function() {
            this.classList.remove('is-invalid');
            const errorMsg = form.querySelector('.invalid-feedback');
            if (errorMsg) errorMsg.style.display = 'none';
            
            const successMsg = form.querySelector('.valid-feedback');
            if (successMsg) successMsg.style.display = 'none';
        });

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            if (!emailInput.value.trim() || !isValidEmail(emailInput.value)) {
                let errorMsg = form.querySelector('.invalid-feedback');
                if (!errorMsg) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'invalid-feedback d-block';
                    emailInput.parentNode.appendChild(errorMsg);
                } else {
                    errorMsg.style.display = 'block';
                }

                errorMsg.textContent = emailInput.value.trim() ? 
                    'Please enter a valid email address' : 
                    'Please enter your email address';
                
                emailInput.classList.add('is-invalid');
                return;
            }

            // Check for disposable email domains
            const disposableDomains = [
                'mailinator.com', 
                'tempmail.com', 
                'throwawaymail.com', 
                'yopmail.com', 
                'guerrillamail.com'
            ];
            
            const emailDomain = emailInput.value.split('@')[1];
            if (emailDomain && disposableDomains.includes(emailDomain)) {
                let errorMsg = form.querySelector('.invalid-feedback');
                if (!errorMsg) {
                    errorMsg = document.createElement('div');
                    errorMsg.className = 'invalid-feedback d-block';
                    emailInput.parentNode.appendChild(errorMsg);
                } else {
                    errorMsg.style.display = 'block';
                }
                errorMsg.textContent = 'Please use a non-disposable email address';
                emailInput.classList.add('is-invalid');
                return;
            }

            // If we get here, form is valid - submit it
            form.submit();
        });
    });
}

// Tab Switching Module
const TabManager = (function() {
    let currentTab = null;
    let tabs = [];
    let forms = [];

    function init() {
        tabs = Array.from(document.querySelectorAll('.auth-tab'));
        forms = Array.from(document.querySelectorAll('.auth-form'));

        if (tabs.length === 0 || forms.length === 0) return;

        // Set up tab click handlers
        tabs.forEach(tab => {
            tab.addEventListener('click', handleTabClick);
        });

        // Handle direct navigation via URL
        const urlParams = new URLSearchParams(window.location.search);
        const tabParam = urlParams.get('tab');

        if (tabParam) {
            // Activate tab from URL
            const tabToActivate = tabs.find(tab => tab.dataset.tab === tabParam);
            if (tabToActivate) {
                activateTab(tabToActivate);
            } else if (tabs.length > 0) {
                // If URL tab is invalid, activate first tab
                activateTab(tabs[0]);
            }
        } else if (tabs.length > 0) {
            // No tab in URL, activate first tab by default
            activateTab(tabs[0]);
        }
    }


    function handleTabClick(event) {
        event.preventDefault();
        activateTab(this);
    }

    function activateTab(tabElement) {
        const tabId = tabElement.dataset.tab;

        // Skip if already active
        if (currentTab === tabId) return;


        // Update active tab
        tabs.forEach(tab => tab.classList.remove('active'));
        tabElement.classList.add('active');

        // Show corresponding form
        forms.forEach(form => {
            form.style.display = form.id === tabId ? 'block' : 'none';
        });

        // Update URL
        updateUrl(tabId);
        currentTab = tabId;
    }


    function updateUrl(tabName) {
        const url = new URL(window.location);
        url.searchParams.set('tab', tabName);
        window.history.pushState({}, '', url);
    }

    return {
        init: init
    };
})();

// Password visibility toggle
const togglePassword = (function() {
    const buttons = document.querySelectorAll('.toggle-password');
    
    function init() {
        if (buttons.length === 0) return;
        
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const input = this.parentNode.querySelector('input');
                if (!input) return;
                
                const icon = this.querySelector('i');
                if (!icon) return;
                
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.classList.remove('bi-eye');
                    icon.classList.add('bi-eye-slash');
                } else {
                    input.type = 'password';
                    icon.classList.remove('bi-eye-slash');
                    icon.classList.add('bi-eye');
                }
            });
        });
    }
    
    return { init };
})();

// Password strength meter
const passwordMeter = (function() {
    const passwordInput = document.getElementById('id_password1');
    const confirmPasswordInput = document.getElementById('id_confirm_password');
    const strengthMeter = document.querySelector('.password-strength');
    
    function init() {
        if (!passwordInput || !strengthMeter) return;
        
        passwordInput.addEventListener('input', updateStrengthMeter);
        
        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', validatePasswordMatch);
        }
    }
    
    function updateStrengthMeter() {
        if (this.value) {
            strengthMeter.classList.remove('d-none');
            updatePasswordStrength(this.value, strengthMeter);
        } else {
            strengthMeter.classList.add('d-none');
        }
    }
    
    function validatePasswordMatch() {
        if (passwordInput && this.value !== passwordInput.value) {
            this.setCustomValidity('Passwords do not match');
        } else {
            this.setCustomValidity('');
        }
    }
    
    return { init };
})();

// Initialize modules when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize tab manager
        TabManager.init();
        
        // Initialize password visibility toggle
        togglePassword.init();
        
        // Initialize password strength meter
        passwordMeter.init();
        
        // Initialize form validation
        const forms = document.querySelectorAll('.needs-validation');
        if (forms.length > 0) {
            forms.forEach(form => {
                form.addEventListener('submit', event => {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                    }
                    form.classList.add('was-validated');
                }, false);
            });
        }
    });
} else {
    // If DOM is already loaded, initialize immediately
    TabManager.init();
    togglePassword.init();
    passwordMeter.init();
    
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length > 0) {
        forms.forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }
}

// End of file
