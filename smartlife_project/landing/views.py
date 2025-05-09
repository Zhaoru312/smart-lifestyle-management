from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import HeroSection, Feature, Testimonial, FAQ
from .forms import ContactForm, FAQForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboardmanager:index')
    
    hero_section = HeroSection.objects.filter(is_active=True).first()
    features = Feature.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'index.html', {
        'hero_section': hero_section,
        'features': features,
        'testimonials': testimonials,
        'faqs': faqs
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Session ends when browser closes
            return redirect('dashboardmanager:index')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password can\'t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can\'t be a commonly used password. Your password can\'t be entirely numeric.'
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboardmanager:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

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
    return render(request, 'faq.html', {'form': form, 'faqs': faqs})

def logout_view(request):
    logout(request)
    return redirect('index')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a random token
            import random
            import string
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            
            # Send reset email
            subject = 'SmartLife - Password Reset Request'
            message = f'''
Dear {user.username},

You have requested to reset your password for your SmartLife account.

Please click on the link below to reset your password:
http://localhost:8000/reset-password/{token}/

If you did not request this password reset, please ignore this email.

Best regards,
SmartLife Team
'''
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('forgot_password')
    
    return render(request, 'forgot_password.html')