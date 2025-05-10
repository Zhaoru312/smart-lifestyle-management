from django import forms
from .models import HeroSection, Feature, Testimonial, FAQ, UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar',
            'bio',
            'birth_date',
            'phone_number',
            'address',
            'website',
            'interests',
            'profession',
            'company',
            'location',
            'notification_email',
            'notification_sms',
            'notification_push'
        ]
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'notification_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_sms': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_push': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class HeroForm(forms.ModelForm):
    call_to_action_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        help_text='Optional: Enter a valid URL for the call to action button'
    )

    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle', 'call_to_action_text', 'call_to_action_url', 'is_active', 'background_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'call_to_action_text': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['title', 'icon', 'description', 'order', 'is_active',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'rating', 'is_active', 'content', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5, 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': True}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
