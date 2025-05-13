from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
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

def auth_view(request):
    """
    Unified authentication view that handles login, registration, and password reset.
    Uses a single template with tabs for different authentication functions.
    """
    # Redirect already logged-in users to dashboard
    if request.user.is_authenticated:
        return redirect(reverse('dashboardmanager:index'))
    
    # Get the active tab from query parameters or set to login by default
    active_tab = request.GET.get('tab', 'login')
    
    # Get the 'next' parameter if present
    next_url = request.GET.get('next', reverse('dashboardmanager:index'))
    
    return render(request, 'landing/auth.html', {
        'active_tab': active_tab,
        'next': next_url
    })

def login_view(request):
    """
    Handle user login with username/password authentication.
    Supports 'remember me' functionality to control session expiry.
    """
    # Redirect already logged-in users to dashboard
    if request.user.is_authenticated:
        return redirect(reverse('dashboardmanager:index'))
    
    # For GET requests, redirect to the unified auth page with login tab active
    if request.method == 'GET':
        return redirect(reverse('landing:auth') + '?tab=login')
    
    # Get the active tab from query parameters or set to login by default
    active_tab = 'login'
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me') == 'on'
        next_url = request.POST.get('next', reverse('dashboardmanager:index'))
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return render(request, 'landing/auth.html', {'active_tab': 'login', 'next': next_url})
            
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is active
            if not user.is_active:
                messages.error(request, 'Your account is disabled. Please contact support.')
                return render(request, 'landing/auth.html', {'active_tab': 'login', 'next': next_url})
                
            # Log in the user
            login(request, user)
            
            # Set session expiry based on remember me checkbox
            if remember_me:
                request.session.set_expiry(SESSION_EXPIRY_NEVER)
            else:
                request.session.set_expiry(SESSION_EXPIRY_BROWSER)
                
            # Update last login time in user profile
            if hasattr(user, 'profile'):
                user.profile.last_activity = timezone.now()
                user.profile.save(update_fields=['last_activity'])
                
            # Redirect to next URL or dashboard
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'landing/auth.html', {'active_tab': 'login', 'next': next_url})
    
    # Get the 'next' parameter if present
    next_url = request.GET.get('next', '')
    return render(request, 'landing/auth.html', {'active_tab': active_tab, 'next': next_url})

def register_view(request):
    """
    Handle user registration with form validation.
    Creates a new user account and automatically logs in the user upon successful registration.
    """
    # Redirect already logged-in users to dashboard
    if request.user.is_authenticated:
        return redirect(reverse('dashboardmanager:index'))
    
    # For GET requests, redirect to the unified auth page with register tab active
    if request.method == 'GET':
        return redirect(reverse('landing:auth') + '?tab=register')
    
    # For POST requests, process the registration form
        
    if request.method == 'POST':
        # Process the form data manually since we're using a custom form in the template
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Create a form instance with the POST data
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            # Create the user account but don't save yet
            user = form.save(commit=False)
            
            # Clean and normalize the username and email
            user.username = form.cleaned_data['username'].lower()
            user.email = form.cleaned_data['email'].lower()
            
            # Set first and last name if provided
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            
            # Save the user
            user.save()
            
            # Create a UserProfile for the new user
            from dashboardmanager.models import UserProfile
            UserProfile.objects.create(user=user)
            
            # Log in the user
            login(request, user)
            
            # Set a welcome message
            messages.success(request, f'Welcome to SmartLife, {user.username}! Your account has been created successfully.')
            
            return redirect(reverse('dashboardmanager:index'))
        else:
            # Format and display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            
            # Return to the register tab with the form errors
            return render(request, 'landing/auth.html', {
                'active_tab': 'register',
                'form_data': request.POST,  # Pass back the submitted data
            })
    
    # For GET requests, just render the template with the register tab active
    return render(request, 'landing/auth.html', {'active_tab': active_tab})

def contact_view(request):
    """
    Handle contact form submissions and display the contact page.
    Saves messages to the database and displays a success message.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact_message = form.save()
            
            # Send notification email to admins (in development this will be printed to console)
            from django.core.mail import mail_admins
            subject = f'New contact message: {contact_message.subject}'
            message = f'''
Name: {contact_message.name}
Email: {contact_message.email}

Message:
{contact_message.message}

View in admin: {request.build_absolute_uri('/admin/landing/contactmessage/')}'''
            mail_admins(subject, message, fail_silently=True)
            
            # Show success message
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            
            # Redirect to a fresh form
            return redirect('landing:contact')
        else:
            # Show error message
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill email if user is logged in
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
            initial['name'] = request.user.get_full_name() or request.user.username
        form = ContactForm(initial=initial)
    
    return render(request, 'landing/contact.html', {'form': form})

def faq_view(request):
    """
    View function for the FAQ page with category support.
    Allows users to browse FAQs by category and submit new questions.
    """
    # Handle form submission for new FAQ questions
    if request.method == 'POST':
        # Only allow authenticated users to submit questions
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to submit a question.')
            return redirect(f"landing:login?next={reverse('landing:faq')}")
            
        form = FAQForm(request.POST)
        if form.is_valid():
            # Save the form but don't commit yet
            faq = form.save(commit=False)
            
            # Set is_active to False so admin can review before publishing
            faq.is_active = False
            
            # Set the user if authenticated
            if request.user.is_authenticated:
                faq.submitted_by = request.user.username
                
            # Save the FAQ
            faq.save()
            
            # Notify admins about the new question
            from django.core.mail import mail_admins
            subject = 'New FAQ question submitted'
            message = f'''
A new FAQ question has been submitted and needs review:

Question: {faq.question}
Category: {faq.category}
Submitted by: {faq.submitted_by or 'Anonymous'}

View in admin: {request.build_absolute_uri('/admin/landing/faq/')}'''
            mail_admins(subject, message, fail_silently=True)
            
            messages.success(request, 'Your question has been submitted successfully! It will be reviewed by our team before being published.')
            return redirect('landing:faq')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FAQForm()
    
    # Get the selected category from the query parameters
    category = request.GET.get('category', None)
    search_query = request.GET.get('q', None)
    
    # Start with all active FAQs
    faqs_query = FAQ.objects.filter(is_active=True)
    
    # Apply category filter if provided
    if category:
        faqs_query = faqs_query.filter(category=category)
        
    # Apply search filter if provided
    if search_query:
        from django.db.models import Q
        faqs_query = faqs_query.filter(
            Q(question__icontains=search_query) | 
            Q(answer__icontains=search_query)
        )
    
    # Get the final ordered queryset
    faqs = faqs_query.order_by('category', 'order')
    
    # Get all unique categories for the filter dropdown
    categories = FAQ.objects.filter(is_active=True).exclude(category='').values_list('category', flat=True).distinct()
    
    context = {
        'form': form,
        'faqs': faqs,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
        'faq_count': faqs.count()
    }
    
    return render(request, 'landing/faq.html', context)

def logout_view(request):
    """
    Handle user logout and redirect to the landing page.
    Clears session data and logs the user out.
    """
    # Log the user out
    logout(request)
    
    # Clear any session data
    request.session.flush()
    
    # Set a success message
    messages.success(request, 'You have been successfully logged out.')
    
    # Redirect to the landing page
    return redirect('landing:index')

def forgot_password_view(request):
    """
    Handle password reset requests.
    Validates email, generates a secure token, and sends reset instructions.
    """
    # Redirect already logged-in users to dashboard
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in. If you want to change your password, please use the profile settings.')
        return redirect(reverse('dashboardmanager:index'))
    
    # For GET requests, redirect to the unified auth page with forgot tab active
    if request.method == 'GET':
        return redirect(reverse('landing:auth') + '?tab=forgot')
        
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        # Basic email validation
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False
            
        if not valid_email:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'landing/auth.html', {'active_tab': 'forgot', 'email': email})
            
        # Check if a user with this email exists
        try:
            user = User.objects.get(email=email)
            
            # Generate a secure token (using Django's built-in token generator)
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            
            # Create a token that expires after a certain time
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build the reset URL
            reset_link = f'{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/'
            
            # In a production environment, send an email with the reset link
            # For development, just print the link to the console
            print(f"Reset link for {user.username}: {reset_link}")
            
            # Send the reset email
            from django.core.mail import send_mail
            subject = 'Password Reset Request'
            message = f'''
Hello {user.username},

You recently requested to reset your password for your SmartLife account.

Please click the link below to reset your password:
{reset_link}

This link will expire in 24 hours.

If you did not request a password reset, please ignore this email or contact support if you have concerns.

Best regards,
The SmartLife Team
'''
            
            send_mail(
                subject,
                message,
                from_email=None,  # Use DEFAULT_FROM_EMAIL from settings
                recipient_list=[email],
                fail_silently=True
            )
            
            # Always show the same message whether the email exists or not (security best practice)
            messages.success(request, 'If an account exists with this email address, you will receive password reset instructions.')
            
        except User.DoesNotExist:
            # For security reasons, don't reveal that the email doesn't exist
            # Instead, show the same success message as if the email was sent
            messages.success(request, 'If an account exists with this email address, you will receive password reset instructions.')
            
        # Redirect to login tab after password reset request
        return redirect(reverse('landing:login') + '?tab=login')
    
    # For GET requests, render the auth template with the forgot tab active
    return render(request, 'landing/auth.html', {'active_tab': active_tab})

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
    """
    Handle newsletter subscription form submissions.
    Validates email, creates subscription record, and sends confirmation email.
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        source = request.POST.get('source', 'website')  # Track where the subscription came from
        
        # Basic email validation
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        
        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False
            
        if valid_email:
            # Check if the email already exists
            from .models import Newsletter
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={
                    'subscription_source': source,
                    'is_active': True
                }
            )
            
            if created:
                # Send confirmation email
                from django.core.mail import send_mail
                subject = 'Welcome to SmartLife Newsletter'
                message = f'''
Thank you for subscribing to the SmartLife newsletter!

You'll now receive updates about new features, tips, and special offers.

If you wish to unsubscribe, please click the unsubscribe link in any of our emails.

Best regards,
The SmartLife Team
'''
                send_mail(
                    subject,
                    message,
                    from_email=None,  # Use DEFAULT_FROM_EMAIL from settings
                    recipient_list=[email],
                    fail_silently=True
                )
                
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                # If the subscription exists but was inactive, reactivate it
                if not newsletter.is_active:
                    newsletter.is_active = True
                    newsletter.subscription_source = source
                    newsletter.save(update_fields=['is_active', 'subscription_source', 'updated_at'])
                    messages.success(request, 'Your newsletter subscription has been reactivated!')
                else:
                    messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    # Redirect back to the referring page or home page
    return redirect(request.META.get('HTTP_REFERER', 'landing:index'))