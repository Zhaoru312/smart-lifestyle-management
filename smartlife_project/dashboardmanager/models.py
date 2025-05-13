from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import escape

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

# Content Management Models
# These models were moved from the landing app to centralize content management

class HeroSection(models.Model):
    """
    Model for the hero section on the landing page.
    Contains title, subtitle, background image, and call-to-action elements.
    """
    title = models.CharField(max_length=200, help_text='Main heading for the hero section')
    subtitle = models.TextField(help_text='Subheading or description text')
    background_image = models.ImageField(
        upload_to='hero_images/', 
        blank=True, 
        null=True, 
        help_text='Background image for the hero section (recommended size: 1920x1080px)'
    )
    call_to_action_text = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text='Text for the call-to-action button (optional)'
    )
    call_to_action_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text='URL for the call-to-action button (optional)'
    )
    is_active = models.BooleanField(default=True, help_text='Whether this hero section is currently displayed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'

    def __str__(self):
        return self.title

class Feature(models.Model):
    """
    Model for features displayed on the landing page.
    Each feature includes a title, description, and icon.
    """
    title = models.CharField(max_length=100, help_text='Title of the feature')
    description = models.TextField(help_text='Description of the feature')
    icon = models.CharField(
        max_length=50, 
        help_text='Font Awesome or Bootstrap icon class (e.g., fa-chart-line, bi-graph-up)'
    )
    order = models.IntegerField(default=0, help_text='Display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True, help_text='Whether this feature is currently displayed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Feature'
        verbose_name_plural = 'Features'

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    """
    Model for testimonials displayed on the landing page.
    Each testimonial includes a person's name, role, content, image, and rating.
    """
    name = models.CharField(max_length=100, help_text='Name of the person giving the testimonial')
    role = models.CharField(max_length=100, help_text='Job title or role of the person')
    content = models.TextField(help_text='The testimonial text')
    image = models.ImageField(
        upload_to='testimonials/',
        help_text='Photo of the person (recommended size: 200x200px, square)'
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text='Rating from 1 to 5 stars'
    )
    is_active = models.BooleanField(default=True, help_text='Whether this testimonial is currently displayed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} - {self.role}"

class FAQ(models.Model):
    """Frequently Asked Questions model for the landing page"""
    question = models.CharField(max_length=200)
    answer = models.TextField(help_text='You can use basic HTML tags for formatting')
    category = models.CharField(max_length=100, blank=True, help_text='Optional category for grouping FAQs')
    submitted_by = models.CharField(max_length=150, blank=True, help_text='Username of the person who submitted this question')
    order = models.IntegerField(default=0, help_text='Controls the display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def safe_answer(self):
        """Return the answer with HTML tags escaped."""
        return escape(self.answer)
    
    @property
    def answer_preview(self):
        """Return a shortened preview of the answer for display in lists"""
        if len(self.answer) > 100:
            return f"{self.answer[:100]}..."
        return self.answer

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    """
    Model for storing contact form submissions.
    Includes sender information and message content.
    """
    name = models.CharField(max_length=100, help_text='Name of the sender')
    email = models.EmailField(help_text='Email address of the sender')
    subject = models.CharField(max_length=200, help_text='Subject of the message')
    message = models.TextField(help_text='Content of the message')
    is_read = models.BooleanField(default=False, help_text='Whether this message has been read by an admin')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True, help_text='When a response was sent')

    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
        
    def mark_as_read(self):
        """Mark the message as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

class Newsletter(models.Model):
    """
    Model for storing newsletter subscriptions.
    Tracks email addresses for sending newsletters and updates.
    """
    email = models.EmailField(unique=True, help_text='Email address for the subscription')
    is_active = models.BooleanField(default=True, help_text='Whether this subscription is currently active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sent_at = models.DateTimeField(null=True, blank=True, help_text='When the last newsletter was sent')
    subscription_source = models.CharField(max_length=50, blank=True, help_text='Where the subscription came from (e.g., footer, popup)')

    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
        
    def unsubscribe(self):
        """Mark the subscription as inactive"""
        if self.is_active:
            self.is_active = False
            self.save(update_fields=['is_active', 'updated_at'])