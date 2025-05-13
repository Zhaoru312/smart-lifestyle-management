from django.contrib import admin
from .models import Feature, Testimonial, FAQ, ContactMessage, HeroSection, Newsletter

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle_preview', 'has_image', 'has_cta', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    actions = ['activate_hero_sections', 'deactivate_hero_sections']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle')
        }),
        ('Image', {
            'fields': ('background_image', 'image_preview')
        }),
        ('Call to Action', {
            'fields': ('call_to_action_text', 'call_to_action_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subtitle_preview(self, obj):
        """Display a preview of the subtitle in the admin list view"""
        if len(obj.subtitle) > 50:
            return f"{obj.subtitle[:50]}..."
        return obj.subtitle
    subtitle_preview.short_description = 'Subtitle'
    
    def has_image(self, obj):
        """Check if hero section has an image"""
        return bool(obj.background_image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def has_cta(self, obj):
        """Check if hero section has a call to action"""
        return bool(obj.call_to_action_text) and bool(obj.call_to_action_url)
    has_cta.boolean = True
    has_cta.short_description = 'Has CTA'
    
    def image_preview(self, obj):
        """Display a preview of the image in the admin detail view"""
        if obj.background_image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 200px; max-width: 400px;" />', obj.background_image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def activate_hero_sections(self, request, queryset):
        """Activate selected hero sections"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} hero section(s) activated.')
    activate_hero_sections.short_description = 'Activate selected hero sections'
    
    def deactivate_hero_sections(self, request, queryset):
        """Deactivate selected hero sections"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} hero section(s) deactivated.')
    deactivate_hero_sections.short_description = 'Deactivate selected hero sections'

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'description_preview', 'icon', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'icon')
    ordering = ('order',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['activate_features', 'deactivate_features']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description')
        }),
        ('Display', {
            'fields': ('icon', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def description_preview(self, obj):
        """Display a preview of the description in the admin list view"""
        if len(obj.description) > 50:
            return f"{obj.description[:50]}..."
        return obj.description
    description_preview.short_description = 'Description'
    
    def activate_features(self, request, queryset):
        """Activate selected features"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} feature(s) activated.')
    activate_features.short_description = 'Activate selected features'
    
    def deactivate_features(self, request, queryset):
        """Deactivate selected features"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} feature(s) deactivated.')
    deactivate_features.short_description = 'Deactivate selected features'

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'content_preview', 'rating', 'has_image', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('name', 'role', 'content')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    actions = ['activate_testimonials', 'deactivate_testimonials']
    
    fieldsets = (
        ('Author Information', {
            'fields': ('name', 'role', 'rating')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        """Display a preview of the content in the admin list view"""
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    content_preview.short_description = 'Content Preview'
    
    def has_image(self, obj):
        """Check if testimonial has an image"""
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'
    
    def image_preview(self, obj):
        """Display a preview of the image in the admin detail view"""
        if obj.image:
            from django.utils.html import format_html
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 50%;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def activate_testimonials(self, request, queryset):
        """Activate selected testimonials"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} testimonial(s) activated.')
    activate_testimonials.short_description = 'Activate selected testimonials'
    
    def deactivate_testimonials(self, request, queryset):
        """Deactivate selected testimonials"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} testimonial(s) deactivated.')
    deactivate_testimonials.short_description = 'Deactivate selected testimonials'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'responded_at', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_responded']
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email')
        }),
        ('Message Content', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'responded_at')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def message_preview(self, obj):
        """Display a preview of the message in the admin list view"""
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = 'Message Preview'
    
    def mark_as_read(self, request, queryset):
        """Mark selected messages as read"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected messages as unread"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')
    mark_as_unread.short_description = 'Mark selected messages as unread'
    
    def mark_as_responded(self, request, queryset):
        """Mark selected messages as responded"""
        from django.utils import timezone
        updated = queryset.update(responded_at=timezone.now())
        self.message_user(request, f'{updated} message(s) marked as responded.')
    mark_as_responded.short_description = 'Mark selected messages as responded'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'answer_preview_admin', 'submitted_by', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('question', 'answer', 'category', 'submitted_by')
    ordering = ('category', 'order')
    list_editable = ('category', 'order', 'is_active')
    readonly_fields = ('submitted_by', 'created_at', 'updated_at')
    actions = ['approve_faqs', 'unapprove_faqs']
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer')
        }),
        ('Categorization', {
            'fields': ('category', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Submission Information', {
            'fields': ('submitted_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def answer_preview_admin(self, obj):
        """Display a preview of the answer in the admin list view"""
        if len(obj.answer) > 50:
            return f"{obj.answer[:50]}..."
        return obj.answer
    answer_preview_admin.short_description = 'Answer Preview'
    
    def approve_faqs(self, request, queryset):
        """Approve selected FAQs (mark as active)"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} FAQ(s) approved and now visible on the site.')
    approve_faqs.short_description = 'Approve selected FAQs'
    
    def unapprove_faqs(self, request, queryset):
        """Unapprove selected FAQs (mark as inactive)"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} FAQ(s) unapproved and hidden from the site.')
    unapprove_faqs.short_description = 'Unapprove selected FAQs'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscription_source', 'last_sent_at', 'created_at')
    list_filter = ('is_active', 'subscription_source', 'created_at')
    search_fields = ('email',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    actions = ['activate_subscriptions', 'deactivate_subscriptions', 'update_last_sent']
    
    fieldsets = (
        ('Subscription Information', {
            'fields': ('email', 'is_active')
        }),
        ('Additional Details', {
            'fields': ('subscription_source', 'last_sent_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def activate_subscriptions(self, request, queryset):
        """Activate selected subscriptions"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscription(s) activated.')
    activate_subscriptions.short_description = 'Activate selected subscriptions'
    
    def deactivate_subscriptions(self, request, queryset):
        """Deactivate selected subscriptions"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscription(s) deactivated.')
    deactivate_subscriptions.short_description = 'Deactivate selected subscriptions'
    
    def update_last_sent(self, request, queryset):
        """Update last sent date to now for selected subscriptions"""
        from django.utils import timezone
        updated = queryset.update(last_sent_at=timezone.now())
        self.message_user(request, f'Last sent date updated for {updated} subscription(s).')
    update_last_sent.short_description = 'Update last sent date to now'
