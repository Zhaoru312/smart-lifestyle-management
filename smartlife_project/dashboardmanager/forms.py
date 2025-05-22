from django import forms
from .models import UserProfile, DashboardBookmark, DashboardNote, DashboardReminder, DashboardShortcut
from .models import HeroSection, Feature, Testimonial, FAQ

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
            'preferred_currency'
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
            'preferred_currency': forms.Select(attrs={'class': 'form-control'}),
        }

class HeroForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle', 'call_to_action_text', 'call_to_action_url', 'is_active', 'background_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'call_to_action_text': forms.TextInput(attrs={'class': 'form-control'}),
            'call_to_action_url': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['title', 'icon', 'description', 'order', 'is_active']
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
        fields = ['name', 'role', 'rating', 'order', 'is_active', 'content', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '5', 
                'required': True,
                'oninput': 'this.value = Math.max(1, Math.min(5, Math.round(this.value)))'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '1',
                'placeholder': 'Leave blank to auto-increment'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError('Rating must be between 1 and 5')
        return rating

class dashboardFAQForm(forms.ModelForm):
    # Define predefined categories
    CATEGORY_CHOICES = [
        ('feature', 'Feature Details'),
        ('support', 'Support & Help'),
        ('usage', 'How to Use'),
        ('troubleshooting', 'Troubleshooting'),
        ('', 'Other')  # Empty value for no category
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category', 'order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Forms for new dashboard models
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = DashboardBookmark
        fields = ['title', 'url', 'description', 'category', 'tags', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = DashboardNote
        fields = ['title', 'content', 'category', 'tags', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReminderForm(forms.ModelForm):
    class Meta:
        model = DashboardReminder
        fields = ['title', 'description', 'reminder_type', 'due_date', 'repeat_interval', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reminder title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional details about this reminder'}),
            'reminder_type': forms.Select(attrs={'class': 'form-control', 'id': 'reminder-type-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'repeat_interval': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Days between repetitions'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['repeat_interval'].help_text = 'Required for custom interval reminders'
        
    def clean(self):
        cleaned_data = super().clean()
        reminder_type = cleaned_data.get('reminder_type')
        repeat_interval = cleaned_data.get('repeat_interval')
        
        if reminder_type == 'custom' and not repeat_interval:
            self.add_error('repeat_interval', 'This field is required for custom interval reminders')
            
        return cleaned_data

class ShortcutForm(forms.ModelForm):
    class Meta:
        model = DashboardShortcut
        fields = ['title', 'icon', 'shortcut_key', 'action', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'shortcut_key': forms.TextInput(attrs={'class': 'form-control'}),
            'action': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


