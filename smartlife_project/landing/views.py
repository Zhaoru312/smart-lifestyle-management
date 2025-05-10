import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .models import Feature, HeroSection, Testimonial, FAQ
from .forms import ContactForm, FAQForm, CustomUserCreationForm

# Constants
SESSION_EXPIRY_NEVER = 1209600  # 2 weeks in seconds
SESSION_EXPIRY_BROWSER = 0  # Session ends when browser closes

# Create your views here.
def index(request):
    # Always show the landing page regardless of authentication status
    if request.method == 'POST':
        # Handle hero section form
        if 'add_hero' in request.POST:
            hero_form = HeroSectionForm(request.POST, request.FILES)
            if hero_form.is_valid():
                hero_form.save()
                messages.success(request, 'Hero section added successfully')
                return redirect('index')
            else:
                messages.error(request, 'Please fix the errors below')
                
        # Handle feature form
        elif 'add_feature' in request.POST:
            feature_form = FeatureForm(request.POST)
            if feature_form.is_valid():
                feature_form.save()
                messages.success(request, 'Feature added successfully')
                return redirect('index')
            else:
                messages.error(request, 'Please fix the errors below')
                
        # Handle testimonial form
        elif 'add_testimonial' in request.POST:
            testimonial_form = TestimonialForm(request.POST, request.FILES)
            if testimonial_form.is_valid():
                testimonial_form.save()
                messages.success(request, 'Testimonial added successfully')
                return redirect('index')
            else:
                messages.error(request, 'Please fix the errors below')
                
        # Handle FAQ form
        elif 'add_faq' in request.POST:
            faq_form = FAQForm(request.POST)
            if faq_form.is_valid():
                faq_form.save()
                messages.success(request, 'FAQ added successfully')
                return redirect('index')
            else:
                messages.error(request, 'Please fix the errors below')
                
    # Initialize forms
    hero_form = HeroSectionForm(request.POST or None, request.FILES or None)
    feature_form = FeatureForm(request.POST or None)
    testimonial_form = TestimonialForm(request.POST or None, request.FILES or None)
    faq_form = FAQForm(request.POST or None)
    
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
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your question has been submitted successfully!')
            return redirect('faq')
    else:
        form = FAQForm()
    
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    return render(request, 'landing/faq.html', {'form': form, 'faqs': faqs})

def logout_view(request):
    logout(request)
    return redirect("/")

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Generate a random token
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