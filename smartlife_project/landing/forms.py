from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from .models import ContactMessage, FAQ, Newsletter

class ContactForm(forms.ModelForm):
    """
    Form for handling contact message submissions.
    Includes validation for all fields and custom error messages.
    """
    # Add additional validation
    name = forms.CharField(
        min_length=2, 
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
            'autocomplete': 'name'
        }),
        help_text='Enter your full name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email',
            'autocomplete': 'email'
        }),
        help_text='We\'ll never share your email with anyone else'
    )
    
    subject = forms.CharField(
        min_length=5,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        }),
        help_text='Brief description of your inquiry'
    )
    
    message = forms.CharField(
        min_length=10,
        validators=[MinLengthValidator(10, 'Your message is too short. Please provide more details.')],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Your Message',
            'rows': 5
        }),
        help_text='Please be as detailed as possible'
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        
    def clean_email(self):
        """Normalize the email address by lowercasing the domain part"""
        email = self.cleaned_data['email']
        if '@' in email:
            local_part, domain = email.rsplit('@', 1)
            email = local_part + '@' + domain.lower()
        return email
        
    def clean_message(self):
        """Check for spam keywords in the message"""
        message = self.cleaned_data['message']
        spam_keywords = ['viagra', 'casino', 'lottery', 'prize', 'winner', 'free money']
        
        for keyword in spam_keywords:
            if keyword in message.lower():
                raise forms.ValidationError(
                    'Your message contains content that appears to be spam. Please revise your message.'
                )
                
        return message

class FAQForm(forms.ModelForm):
    """
    Form for handling FAQ submissions.
    Allows users to submit questions that will be reviewed by admins.
    """
    question = forms.CharField(
        min_length=10,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Question',
        }),
        help_text='Be specific and clear with your question'
    )
    
    answer = forms.CharField(
        required=False,  # Allow users to submit questions without answers
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Suggested Answer (Optional)',
            'rows': 5
        }),
        help_text='If you know the answer, you can suggest it here'
    )
    
    category = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Category (Optional)'
        }),
        help_text='Optional category to help organize your question'
    )
    
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category']
        
    def clean_question(self):
        """Ensure the question ends with a question mark and isn't a duplicate"""
        question = self.cleaned_data['question']
        
        # Add a question mark if not present
        if not question.strip().endswith('?'):
            question = question.strip() + '?'
            
        # Check for duplicates
        if FAQ.objects.filter(question__iexact=question).exists():
            raise forms.ValidationError(
                'This question has already been asked. Please check the existing FAQs.'
            )
            
        return question

class CustomUserCreationForm(UserCreationForm):
    """
    Enhanced user registration form with additional fields and validation.
    Includes email field and improved styling for all form elements.
    """
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'autocomplete': 'given-name'
        }),
        help_text='Optional. Your first name.'
    )
    
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'autocomplete': 'family-name'
        }),
        help_text='Optional. Your last name.'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'autocomplete': 'email'
        }),
        help_text='Required. Enter a valid email address. This will be used for account recovery.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Improve field styling and help text
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete': 'username'
        })
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        })
        self.fields['password1'].help_text = 'Your password must be at least 8 characters long and cannot be entirely numeric.'
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].help_text = 'Enter the same password as before, for verification.'
        
    def clean_email(self):
        """Validate that the email is not already in use"""
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use. Please use a different email or try to log in.')
        return email
        
    def clean_username(self):
        """Convert username to lowercase for consistency"""
        username = self.cleaned_data.get('username').lower()
        return username
        
    def save(self, commit=True):
        """Save the user with normalized data"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.username = self.cleaned_data['username'].lower()
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
            
        return user
class NewsletterForm(forms.ModelForm):
    """
    Form for newsletter subscriptions.
    Simple form with just an email field and validation.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email Address',
            'autocomplete': 'email'
        }),
        help_text='Enter your email to receive updates and news'
    )
    
    class Meta:
        model = Newsletter
        fields = ['email']
        
    def clean_email(self):
        """Normalize and validate the email address"""
        email = self.cleaned_data.get('email', '').lower()
        
        # Check if already subscribed
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('This email is already subscribed to our newsletter.')
            
        # Check for disposable email domains
        disposable_domains = ['tempmail.com', 'throwawaymail.com', 'mailinator.com', 'yopmail.com']
        if '@' in email:
            domain = email.split('@')[1]
            if domain in disposable_domains:
                raise forms.ValidationError('Please use a permanent email address for subscription.')
                
        return email
