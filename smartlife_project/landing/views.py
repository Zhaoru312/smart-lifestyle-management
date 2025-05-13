from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Feature, HeroSection, Testimonial, FAQ
from .forms import ContactForm, FAQForm, CustomUserCreationForm
from dashboardmanager.forms import HeroForm, FeatureForm, TestimonialForm, FAQForm
    
# Constants
SESSION_EXPIRY_NEVER = 1209600  # 2 weeks in seconds
SESSION_EXPIRY_BROWSER = 0  # Session ends when browser closes

def index(request):
    """
    Landing page view that handles form submissions for hero sections, features,
    testimonials, and FAQs.
    """
    # Initialize forms
    hero_form = HeroForm(request.POST or None, request.FILES or None)
    feature_form = FeatureForm(request.POST or None)
    testimonial_form = TestimonialForm(request.POST or None, request.FILES or None)
    faq_form = FAQForm(request.POST or None)

    if request.method == 'POST':
        # Handle form submissions
        if 'add_hero' in request.POST and hero_form.is_valid():
            hero_form.save()
            messages.success(request, 'Hero section added successfully')
            return redirect('index')
        
        elif 'add_feature' in request.POST and feature_form.is_valid():
            feature_form.save()
            messages.success(request, 'Feature added successfully')
            return redirect('index')
        
        elif 'add_testimonial' in request.POST and testimonial_form.is_valid():
            testimonial_form.save()
            messages.success(request, 'Testimonial added successfully')
            return redirect('index')
        
        elif 'add_faq' in request.POST and faq_form.is_valid():
            faq_form.save()
            messages.success(request, 'FAQ added successfully')
            return redirect('index')
        
        # If any form is invalid
        messages.error(request, 'Please fix the errors below')

    context = {
        'hero_sections': HeroSection.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'faqs': FAQ.objects.filter(is_active=True)[:3],
        'user': request.user if request.user.is_authenticated else None,
        'apps': Feature.objects.filter(is_active=True),
        'hero_form': hero_form,
        'feature_form': feature_form,
        'testimonial_form': testimonial_form,
        'faq_form': faq_form,
        'show_messages': True
    }
    
    return render(request, 'landing/index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(SESSION_EXPIRY_NEVER)
            else:
                request.session.set_expiry(SESSION_EXPIRY_BROWSER)
            return redirect(reverse('dashboardmanager:index'))
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'landing/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboardmanager:index'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'landing/register.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('landing:contact')
    else:
        form = ContactForm()
    
    return render(request, 'landing/contact.html', {'form': form})

def faq_view(request):
    """View function for the FAQ page with category support"""
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your question has been submitted successfully!')
            return redirect('landing:faq')
    else:
        form = FAQForm()
    
    # Get the selected category from the query parameters
    category = request.GET.get('category', None)
    
    # Filter FAQs based on category if provided
    if category:
        faqs = FAQ.objects.filter(is_active=True, category=category).order_by('order')
    else:
        # Get all FAQs, ordered first by category, then by order
        faqs = FAQ.objects.filter(is_active=True).order_by('category', 'order')
    
    # Get all unique categories for the filter dropdown
    categories = FAQ.objects.filter(is_active=True).exclude(category='').values_list('category', flat=True).distinct()
    
    context = {
        'form': form,
        'faqs': faqs,
        'categories': categories,
        'selected_category': category
    }
    
    return render(request, 'landing/faq.html', context)

def logout_view(request):
    logout(request)
    return redirect("/")

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate a random token
            import random, string
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            # For development, just print the reset link
            reset_link = f'{request.scheme}://{request.get_host()}/reset-password/{token}/'
            print(f"Reset link for {user.username}: {reset_link}")
            
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('landing:forgot_password')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('landing:forgot_password')
    
    return render(request, 'landing/forgot_password.html')

# Custom error views
def custom_404_view(request, exception):
    """Custom 404 page not found error view"""
    return render(request, 'landing/errors/404.html', status=404)

def custom_500_view(request):
    """Custom 500 server error view"""
    return render(request, 'landing/errors/500.html', status=500)

def custom_403_view(request, exception):
    """Custom 403 permission denied error view"""
    return render(request, 'landing/errors/403.html', status=403)


def newsletter_subscribe(request):
    """Handle newsletter subscription form submissions"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if the email already exists
            from .models import Newsletter
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            
            if created:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    # Redirect back to the referring page or home page
    return redirect(request.META.get('HTTP_REFERER', 'landing:index'))