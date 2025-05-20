from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse,reverse_lazy
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Q
from django.core.mail import mail_admins, send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import TemplateView, FormView, RedirectView

# Local imports
from dashboardmanager.models import Feature, HeroSection, Testimonial, FAQ, Newsletter, UserProfile
from .forms import ContactForm, CustomUserCreationForm

class IndexView(TemplateView):
    """
    Landing page view that handles form submissions for hero sections, features,
    testimonials, and FAQs.
    """
    template_name = 'landing/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add data to context
        context['hero_sections'] = HeroSection.objects.filter(is_active=True)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
        context['faqs'] = FAQ.objects.filter(is_active=True)[:3]
        context['user'] = self.request.user if self.request.user.is_authenticated else None
        context['apps'] = Feature.objects.filter(is_active=True)
        context['show_messages'] = True
        
        return context

class AuthView(TemplateView):
    """
    Unified authentication view that handles login, registration, and password reset.
    Uses a single template with tabs for different authentication functions.
    """
    template_name = 'landing/auth.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect already logged-in users to dashboard
        if request.user.is_authenticated:
            return RedirectView.as_view(url=reverse('dashboardmanager:index'))(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the active tab from query parameters or set to login by default
        context['active_tab'] = self.request.GET.get('tab', 'login')
        
        # Get the 'next' parameter if present
        context['next'] = self.request.GET.get('next', reverse('landing:login'))
        
        return context

class LoginView(TemplateView):
    """
    Handle user login with username/password authentication.
    Supports 'remember me' functionality to control session expiry.
    """
    # Constants
    SESSION_EXPIRY_NEVER = 1209600  # 2 weeks in seconds
    SESSION_EXPIRY_BROWSER = 0  # Session ends when browser closes
    
    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me') == 'on'
        next_url = request.POST.get('next', reverse('dashboardmanager:index'))
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return RedirectView.as_view(url=reverse('landing:auth') + '?tab=login&next=' + next_url)(request)
            
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is active
            if not user.is_active:
                messages.error(request, 'Your account is disabled. Please contact support.')
                return RedirectView.as_view(url=reverse('landing:auth') + '?tab=login&next=' + next_url)(request)
                
            # Log in the user
            login(request, user)
            
            # Set session expiry based on remember me checkbox
            if remember_me:
                request.session.set_expiry(self.SESSION_EXPIRY_NEVER)
            else:
                request.session.set_expiry(self.SESSION_EXPIRY_BROWSER)
                
            # Update last login time in user profile
            if hasattr(user, 'profile'):
                user.profile.last_activity = timezone.now()
                user.profile.save(update_fields=['last_activity'])
                
            # Redirect to next URL or dashboard
            messages.success(request, f'Welcome back SmartLife, {user.username}!.')
            return RedirectView.as_view(url=next_url)(request)
        else:
            messages.error(request, 'Invalid username or password')
            return RedirectView.as_view(url=reverse('landing:auth') + '?tab=login&next=' + next_url)(request)

class RegisterView(TemplateView):
    """
    Handle user registration with form validation.
    Creates a new user account and automatically logs in the user upon successful registration.
    """
    template_name = 'landing/auth.html'
    form_class = CustomUserCreationForm
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect already logged-in users to dashboard
        if request.user.is_authenticated:
            return RedirectView.as_view(url=reverse('dashboardmanager:index'))(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        # For GET requests, redirect to the unified auth page with register tab active
        return RedirectView.as_view(url=reverse('landing:auth') + '?tab=register')(request)
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            # Save the user - our form.save() method handles password hashing
            user = form.save()
            
            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user)
            
            # Log in the user
            login(request, user)
            
            # Set a welcome message
            messages.success(request, f'Welcome to SmartLife, {user.username}! Your account has been created successfully.')
            return RedirectView.as_view(url=reverse('dashboardmanager:index'))(request)
        else:
            # Format and display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            
            # Return to the register tab with the form errors
            return RedirectView.as_view(url=reverse('landing:auth') + '?tab=register')(request)

class ContactView(FormView):
    """
    Handle contact form submissions and display the contact page.
    Saves messages to the database and displays a success message.
    """
    template_name = 'landing/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('landing:contact')
    
    def get_initial(self):
        """Pre-fill form with user data if logged in"""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
            initial['name'] = self.request.user.get_full_name() or self.request.user.username
        return initial
    
    def form_valid(self, form):
        # Save the contact message
        contact_message = form.save()
        
        # Send notification email to admins
        subject = f'New contact message: {contact_message.subject}'
        message = f'''
        Name: {contact_message.name}
        Email: {contact_message.email}

        Message:
        {contact_message.message}

        View in admin: {self.request.build_absolute_uri('/admin/landing/contactmessage/')}'''
        mail_admins(subject, message, fail_silently=True)
        
        # Show success message
        messages.success(self.request, 'Your message has been sent successfully! We will get back to you soon.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle invalid form submission"""
        messages.error(self.request, 'Please correct the errors below. either longer than 10 characters or less than 100 characters')
        return super().form_invalid(form)

class FAQView(TemplateView):
    """
    View for the FAQ page with category support.
    Allows users to browse FAQs by category and submit new questions.
    """
    template_name = 'landing/faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the selected category from the query parameters
        category = self.request.GET.get('category', None)
        
        # Get the search query from the query parameters
        search_query = self.request.GET.get('q', None)
        
        # Query FAQs that are active and order them by category and order
        faqs_query = FAQ.objects.filter(is_active=True)
        
        # Filter by category if one is selected
        if category:
            faqs_query = faqs_query.filter(category=category)
            
        # Search through questions and answers if a search query is provided
        if search_query:
            faqs_query = faqs_query.filter(
                Q(question__icontains=search_query) | 
                Q(answer__icontains=search_query)
            )
        
        # Get the distinct categories for the filter
        categories = FAQ.objects.filter(is_active=True).exclude(category='').values_list('category', flat=True).distinct()
        
        # Get the FAQs and count them
        faqs = faqs_query.order_by('category', 'order')
        
        # Add FAQ data to context
        context = {
            'faqs': faqs,
            'categories': categories,
            'selected_category': category,
            'search_query': search_query,
            'faq_count': faqs.count()
        }
        
        return context

class LogoutView(TemplateView):
    """
    Handle user logout and redirect to the landing page.
    Clears session data and logs the user out.
    """
    def get(self, request):
        # Log the user out
        logout(request)
        
        # Clear any session data
        request.session.flush()
        
        # Set a success message
        messages.success(request, 'You have been successfully logged out.')
        
        # Redirect to the landing page
        return RedirectView.as_view(url=reverse('landing:index'))(request)

class ForgotPasswordView(TemplateView):
    """
    Handle password reset requests.
    Validates email, generates a secure token, and sends reset instructions.
    """
    template_name = 'landing/forgot_password.html'
    
    def dispatch(self, request):
        # Redirect already logged-in users to dashboard
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in. If you want to change your password, please use the profile settings.')
            return redirect(reverse('dashboardmanager:index'))
        return super().dispatch(request)
    
    def get(self, request):
        # For GET requests, redirect to the unified auth page with forgot tab active
        return RedirectView.as_view(url=reverse('landing:auth') + '?tab=forgot')(request)
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        
        # Basic email validation
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
            
            # Create a token that expires after a certain time
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build the reset URL
            reset_link = f'{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/'
            
            # In a production environment, this will use the configured email backend
            # For development with console backend, the email will be printed to the console
            
            # Send the reset email
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
        return RedirectView.as_view(url=reverse('landing:auth') + '?tab=login')(request)

class NewsletterSubscribeView(TemplateView):
    """
    Handle newsletter subscription form submissions.
    Validates email, creates subscription record, and sends confirmation email.
    """
    template_name = 'landing/newsletter_subscribe.html'
    
    def post(self, request):
        email = request.POST.get('email', '').strip().lower()
        source = request.POST.get('source', 'website')  # Track where the subscription came from
        
        # Basic email validation
        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False
            
        if valid_email:
            # Check if the email already exists
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={
                    'subscription_source': source,
                    'is_active': True
                }
            )
            
            if created:
                # Send confirmation email
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
        return RedirectView.as_view(url=request.META.get('HTTP_REFERER', reverse('landing:index')))(request)