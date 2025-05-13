from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# User Profile Model
class UserProfile(models.Model):
    """
    User profile model extending the built-in Django User model.
    Stores additional information about users including personal details,
    preferences, and profile customization options.
    """
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('IDR', 'Indonesian Rupiah'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('SGD', 'Singapore Dollar')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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
    preferred_currency = models.CharField(max_length=3, default='USD', choices=CURRENCY_CHOICES)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-last_activity']

    def __str__(self):
        return f"Profile for {self.user.username}"

    def get_age(self):
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboardmanager:profile')
        
    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

# Dashboard Bookmarks
class DashboardBookmark(models.Model):
    """
    Model for storing user bookmarks in the dashboard.
    Allows users to save and organize important links with categories and tags.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    title = models.CharField(max_length=200, help_text='Name of the bookmark')
    url = models.URLField(help_text='URL of the bookmark')
    description = models.TextField(blank=True, help_text='Optional description of the bookmark')
    category = models.CharField(max_length=50, blank=True, help_text='Category for organizing bookmarks')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    is_favorite = models.BooleanField(default=False, help_text='Mark as a favorite for quick access')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Bookmark'
        verbose_name_plural = 'Dashboard Bookmarks'
        ordering = ['-is_favorite', '-created_at']
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboardmanager:edit_bookmark', kwargs={'pk': self.pk})
        
    def get_tag_list(self):
        """Return tags as a list"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]

# Dashboard Notes
class DashboardNote(models.Model):
    """
    Model for storing user notes in the dashboard.
    Allows users to create and organize notes with categories and tags.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200, help_text='Title of the note')
    content = models.TextField(help_text='Content of the note')
    category = models.CharField(max_length=50, blank=True, help_text='Category for organizing notes')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    is_pinned = models.BooleanField(default=False, help_text='Pin note to top of list')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Note'
        verbose_name_plural = 'Dashboard Notes'
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboardmanager:edit_note', kwargs={'pk': self.pk})
        
    def get_tag_list(self):
        """Return tags as a list"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',')]
        
    def get_summary(self, chars=100):
        """Return a summary of the content"""
        if len(self.content) <= chars:
            return self.content
        return self.content[:chars] + '...'

# Dashboard Reminders
class DashboardReminder(models.Model):
    """
    Model for storing user reminders in the dashboard.
    Supports one-time and recurring reminders with customizable intervals.
    """
    REMINDER_TYPES = [
        ('one_time', 'One Time'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom Interval')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200, help_text='Title of the reminder')
    description = models.TextField(blank=True, help_text='Optional description or details')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES, help_text='Type of reminder recurrence')
    due_date = models.DateTimeField(help_text='When the reminder is due')
    repeat_interval = models.IntegerField(null=True, blank=True, help_text='Interval in days for repeating reminders')
    is_completed = models.BooleanField(default=False, help_text='Mark if the reminder has been completed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Reminder'
        verbose_name_plural = 'Dashboard Reminders'
        ordering = ['is_completed', 'due_date']
    
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboardmanager:edit_reminder', kwargs={'pk': self.pk})
        
    def is_overdue(self):
        """Check if the reminder is overdue"""
        if self.is_completed:
            return False
        return timezone.now() > self.due_date
        
    def get_next_occurrence(self):
        """Calculate the next occurrence based on reminder type and repeat interval"""
        if self.reminder_type == 'one_time' or not self.repeat_interval:
            return None
            
        if self.is_completed:
            base_date = timezone.now()
        else:
            base_date = self.due_date
            
        if self.reminder_type == 'daily':
            return base_date + timezone.timedelta(days=self.repeat_interval)
        elif self.reminder_type == 'weekly':
            return base_date + timezone.timedelta(weeks=self.repeat_interval)
        elif self.reminder_type == 'monthly':
            # Simple approximation for monthly
            return base_date + timezone.timedelta(days=30 * self.repeat_interval)
        return None

# Dashboard Shortcuts
class DashboardShortcut(models.Model):
    """
    Model for storing user shortcuts in the dashboard.
    Allows users to create keyboard shortcuts for frequently used actions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shortcuts')
    title = models.CharField(max_length=100, help_text='Name of the shortcut')
    icon = models.CharField(max_length=50, help_text='FontAwesome icon class (e.g., fa-home)')
    shortcut_key = models.CharField(max_length=20, help_text='Keyboard shortcut (e.g., Ctrl+H)')
    action = models.CharField(max_length=200, help_text='URL or action to perform')
    description = models.TextField(blank=True, help_text='Optional description of what the shortcut does')
    is_active = models.BooleanField(default=True, help_text='Whether the shortcut is currently active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dashboard Shortcut'
        verbose_name_plural = 'Dashboard Shortcuts'
        ordering = ['shortcut_key']
    
    def __str__(self):
        return f"{self.title} ({self.shortcut_key})"
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dashboardmanager:edit_shortcut', kwargs={'pk': self.pk})