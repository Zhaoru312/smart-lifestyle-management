from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, DashboardBookmark, DashboardNote, DashboardReminder, DashboardShortcut

# Admin configuration for the Dashboard Manager app
# This file defines how the models are displayed in the Django admin interface

# Custom admin classes for better organization
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'profession', 'location', 'last_activity', 'profile_status')
    search_fields = ('user__username', 'user__email', 'profession', 'location')
    list_filter = ('preferred_currency', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'last_activity', 'user_email', 'profile_status')
    
    def user_email(self, obj):
        """Display the user's email in the admin list view"""
        return obj.user.email if obj.user else '-'
    user_email.short_description = 'Email'
    
    def profile_status(self, obj):
        """Display a colored status indicator based on profile completeness"""
        # Check if important fields are filled
        fields_to_check = [obj.bio, obj.profession, obj.phone_number]
        filled_fields = sum(1 for field in fields_to_check if field)
        completeness = filled_fields / len(fields_to_check)
        
        if completeness >= 0.8:
            return format_html('<span style="color: green;">Complete</span>')
        elif completeness >= 0.5:
            return format_html('<span style="color: orange;">Partial</span>')
        else:
            return format_html('<span style="color: red;">Incomplete</span>')
    profile_status.short_description = 'Profile Status'
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'avatar', 'bio', 'birth_date')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'website')
        }),
        ('Professional Details', {
            'fields': ('profession', 'company', 'location')
        }),
        ('Preferences', {
            'fields': ('preferred_currency', 'interests', 'social_media')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_activity'),
            'classes': ('collapse',)
        }),
    )

class DashboardBookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_favorite', 'created_at', 'url_link')
    list_filter = ('is_favorite', 'category', 'created_at')
    search_fields = ('title', 'description', 'url', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'url_link')
    
    def url_link(self, obj):
        """Display a clickable link to the bookmark URL"""
        if obj.url:
            return format_html('<a href="{}" target="_blank">Visit Link</a>', obj.url)
        return '-'
    url_link.short_description = 'Visit'

class DashboardNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_pinned', 'created_at')
    list_filter = ('is_pinned', 'category')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

class DashboardReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'reminder_type', 'due_date', 'is_completed', 'status_badge')
    list_filter = ('reminder_type', 'is_completed', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'status_badge')
    actions = ['mark_as_completed', 'mark_as_pending']
    
    def status_badge(self, obj):
        """Display a colored status badge based on completion and due date"""
        from django.utils import timezone
        
        if obj.is_completed:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 10px;">Completed</span>')
        elif obj.due_date and obj.due_date < timezone.now():
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 10px;">Overdue</span>')
        else:
            return format_html('<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 10px;">Pending</span>')
    status_badge.short_description = 'Status'
    
    def mark_as_completed(self, request, queryset):
        """Admin action to mark selected reminders as completed"""
        queryset.update(is_completed=True)
        self.message_user(request, f'{queryset.count()} reminder(s) marked as completed.')
    mark_as_completed.short_description = 'Mark selected reminders as completed'
    
    def mark_as_pending(self, request, queryset):
        """Admin action to mark selected reminders as pending"""
        queryset.update(is_completed=False)
        self.message_user(request, f'{queryset.count()} reminder(s) marked as pending.')
    mark_as_pending.short_description = 'Mark selected reminders as pending'

class DashboardShortcutAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'shortcut_key', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description', 'action', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

# Register models with their admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DashboardBookmark, DashboardBookmarkAdmin)
admin.site.register(DashboardNote, DashboardNoteAdmin)
admin.site.register(DashboardReminder, DashboardReminderAdmin)
admin.site.register(DashboardShortcut, DashboardShortcutAdmin)
