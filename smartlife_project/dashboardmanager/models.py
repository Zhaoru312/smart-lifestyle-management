from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Define widget types
WIDGET_TYPES = (
    ('stats', 'Statistics'),
    ('chart', 'Chart'),
    ('list', 'List'),
    ('custom', 'Custom')
)

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, help_text='Tell us about yourself')
    birth_date = models.DateField(null=True, blank=True, help_text='Your date of birth')
    phone_number = models.CharField(max_length=20, blank=True, help_text='Your contact number')
    address = models.TextField(blank=True, help_text='Your home or office address')
    website = models.URLField(blank=True, help_text='Your personal or business website')
    social_media = models.JSONField(default=dict, help_text='Your social media profiles', blank=True)
    interests = models.TextField(blank=True, help_text='Your hobbies and interests')
    profession = models.CharField(max_length=100, blank=True, help_text='Your current profession or job title')
    company = models.CharField(max_length=100, blank=True, help_text='Your current company or organization')
    location = models.CharField(max_length=100, blank=True, help_text='Your current location/city')
    preferred_currency = models.CharField(max_length=3, default='USD', choices=[
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('IDR', 'Indonesian Rupiah')
    ])
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    notification_push = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    def get_age(self):
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

# Dashboard Widget Model
class DashboardWidget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    width = models.IntegerField(default=6)
    height = models.IntegerField(default=4)
    config = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position_y', 'position_x']

    def __str__(self):
        return f"{self.title} ({self.get_widget_type_display()})"

# User Preferences Model
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, default='light')
    layout = models.CharField(max_length=20, default='grid')
    notifications_enabled = models.BooleanField(default=True)
    last_seen_dashboard = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"

# Dashboard Notification Model
class DashboardNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    category = models.CharField(max_length=20, choices=[
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('success', 'Success')
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.user.username}"

# Dashboard Layout Model
class DashboardLayout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    layout_data = models.JSONField()
    is_default = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.name} for {self.user.username}"

    def save(self, *args, **kwargs):
        # Ensure only one layout per user can be default
        if self.is_default:
            DashboardLayout.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
