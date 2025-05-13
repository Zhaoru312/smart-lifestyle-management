from django.db import models

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

class FAQ(models.Model):
    """Frequently Asked Questions model for the landing page"""
    question = models.CharField(max_length=200)
    answer = models.TextField(help_text='You can use basic HTML tags for formatting')
    category = models.CharField(max_length=100, blank=True, help_text='Optional category for grouping FAQs')
    submitted_by = models.CharField(max_length=150, blank=True, help_text='Username of the person who submitted this question')
    
    @property
    def safe_answer(self):
        """Return the answer with HTML tags escaped."""
        from django.utils.html import escape
        return escape(self.answer)
    
    @property
    def answer_preview(self):
        """Return a shortened preview of the answer for display in lists"""
        if len(self.answer) > 100:
            return f"{self.answer[:100]}..."
        return self.answer

    order = models.IntegerField(default=0, help_text='Controls the display order (lower numbers appear first)')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


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
