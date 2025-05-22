# Django imports
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.utils import timezone
from django.urls import reverse_lazy
import uuid

# Local application imports
from .models import UserProfile, DashboardBookmark, DashboardNote, DashboardReminder, DashboardShortcut
from .models import HeroSection, Feature, Testimonial, FAQ
from .forms import (
    ProfileForm, HeroForm, FeatureForm, TestimonialForm, dashboardFAQForm,
    BookmarkForm, NoteForm, ReminderForm, ShortcutForm
)
class BaseDashboardView(LoginRequiredMixin):
    """Base view for all dashboard views that require login"""
    login_url = settings.LOGIN_URL
    success_message = None
    
    def get_success_url(self):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().get_success_url()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure user is superuser and provides common admin methods"""
    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to access this page.')
        return redirect('dashboardmanager:index')
    
    def handle_form_errors(self, form):
        """Display form errors as messages"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")

class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view showing user's overview and recent activity"""
    template_name = 'dashboardmanager/index.html'
    login_url = settings.LOGIN_URL
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get dashboard statistics
        stats = {
            'total_expenses': 1234.56,
            'workout_streak': 14,
            'active_habits': 5,
            'pending_tasks': 3
        }
        
        # Get user's dashboard items
        context.update({
            'stats': stats,
            'recent_activity': self._get_recent_activity(),
            'bookmarks': DashboardBookmark.objects.filter(user=self.request.user)
                .order_by('-is_favorite', '-created_at')[:3],
            'notes': DashboardNote.objects.filter(user=self.request.user)
                .order_by('-is_pinned', '-created_at')[:3],
            'reminders': DashboardReminder.objects.filter(user=self.request.user)
                .order_by('is_completed', 'due_date')[:3],
            'shortcuts': DashboardShortcut.objects.filter(
                user=self.request.user, 
                is_active=True
            ).order_by('shortcut_key')[:3],
        })
        return context
    
    def _get_recent_activity(self):
        """Helper method to get recent user activity"""
        return [
            {
                'date': '2025-05-09',
                'activity': 'Completed morning workout',
                'category': 'Fitness',
                'status': 'completed'
            },
            {
                'date': '2025-05-09',
                'activity': 'Logged daily expenses',
                'category': 'Finance',
                'status': 'completed'
            },
            {
                'date': '2025-05-09',
                'activity': 'Checked meditation habit',
                'category': 'Habit',
                'status': 'completed'
            },
            {
                'date': '2025-05-09',
                'activity': 'Logged dinner meal',
                'category': 'Meal',
                'status': 'completed'
            }
        ]

class AppListView(LoginRequiredMixin, TemplateView):
    """View showing list of all available applications"""
    template_name = 'dashboardmanager/applist.html'
    login_url = settings.LOGIN_URL
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        apps = [
            {'name': 'Finance', 'url': '/finance/', 'icon': 'fas fa-wallet', 'description': 'Manage your finances and track expenses'},
            {'name': 'Fitness', 'url': '/fitness/', 'icon': 'fas fa-dumbbell', 'description': 'Track your workouts and fitness goals'},
            {'name': 'Habit', 'url': '/habit/', 'icon': 'fas fa-check-circle', 'description': 'Build and track your habits'},
            {'name': 'Meal', 'url': '/meal/', 'icon': 'fas fa-utensils', 'description': 'Log and plan your meals'},
            {'name': 'Mental', 'url': '/mental/', 'icon': 'fas fa-brain', 'description': 'Track your mental health and mood'},
            {'name': 'Tasks', 'url': '/tasks/', 'icon': 'fas fa-tasks', 'description': 'Manage your daily tasks and to-do list'}
        ]
        
        if self.request.user.is_superuser:
            apps.append({
                'name': 'Landing Page', 
                'url': '/dashboard/landing/', 
                'icon': 'fas fa-home',
                'description': 'Manage the landing page content'
            })
            
        context['apps'] = apps
        return context

class ProfileView(LoginRequiredMixin, UpdateView):
    """View for user profile management"""
    model = UserProfile
    form_class = ProfileForm
    template_name = 'dashboardmanager/profile.html'
    success_url = reverse_lazy('dashboardmanager:profile')
    login_url = settings.LOGIN_URL
    
    def get_object(self, queryset=None):
        """Get or create user profile"""
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=self.request.user)
    
    def get_initial(self):
        """Initialize form with current profile data"""
        initial = super().get_initial()
        profile = self.get_object()
        initial.update({
            'bio': profile.bio,
            'birth_date': profile.birth_date,
            'phone_number': profile.phone_number,
            'address': profile.address,
            'website': profile.website,
            'interests': profile.interests,
            'profession': profile.profession,
            'company': profile.company,
            'location': profile.location,
            'preferred_currency': profile.preferred_currency,
        })
        return initial
    
    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        context['profile'] = self.get_object()
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        """Handle form validation and file uploads"""
        profile = form.save(commit=False)
        profile.user = self.request.user
        
        # Handle avatar upload
        if 'avatar' in self.request.FILES:
            self._handle_avatar_upload(profile)
        
        # Handle social media updates
        self._update_social_media(profile)
        
        # Save the profile
        profile.save()
        form.save_m2m()  # Save many-to-many fields if any
        messages.success(self.request, 'Profile updated successfully')
        return super().form_valid(form)
    
    def _handle_avatar_upload(self, profile):
        """Helper method to handle avatar upload"""
        avatar = self.request.FILES['avatar']
        
        # Delete old avatar if exists
        if profile.avatar:
            try:
                default_storage.delete(profile.avatar.path)
            except:
                pass

        # Save new avatar with unique filename
        filename = f"profile_avatars/{self.request.user.username}_{uuid.uuid4()}.jpg"
        with default_storage.open(filename, 'wb') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        profile.avatar = filename
    
    def _update_social_media(self, profile):
        """Helper method to update social media links"""
        if all(key in self.request.POST for key in ['social_media_platform', 'social_media_url']):
            platform = self.request.POST.get('social_media_platform')
            url = self.request.POST.get('social_media_url')
            if platform and url:
                social_media = profile.social_media or {}
                social_media[platform] = url
                profile.social_media = social_media

class LandingPageView(AdminRequiredMixin, TemplateView):
    """View for managing landing page content"""
    template_name = 'dashboardmanager/landing_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'hero_sections': HeroSection.objects.all().order_by('-is_active', 'id'),
            'features': Feature.objects.all().order_by('order', '-is_active'),
            'testimonials': Testimonial.objects.all().order_by('-is_active', 'id'),
            'faqs': FAQ.objects.all().order_by('order', '-is_active'),
            'hero_form': HeroForm(),
            'feature_form': FeatureForm(),
            'testimonial_form': TestimonialForm(),
            'faq_form': dashboardFAQForm()
        })
        return context
    
    def post(self, request, *args, **kwargs):
        form_class = None
        success_message = None
        
        if 'add_hero' in request.POST:
            form_class = HeroForm
            success_message = 'Hero section added successfully'
        elif 'add_feature' in request.POST:
            form_class = FeatureForm
            success_message = 'Feature added successfully'
        elif 'add_testimonial' in request.POST:
            form_class = TestimonialForm
            success_message = 'Testimonial added successfully'
        elif 'add_faq' in request.POST:
            form_class = dashboardFAQForm
            success_message = 'FAQ added successfully'
        
        if form_class and success_message:
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                if hasattr(obj, 'call_to_action_url') and not obj.call_to_action_url:
                    obj.call_to_action_url = None
                obj.save()
                messages.success(request, success_message)
                return redirect('dashboardmanager:landing_page')
            else:
                self.handle_form_errors(form)
        
        return self.get(request, *args, **kwargs)

class HeroSectionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """View for updating a hero section"""
    model = HeroSection
    form_class = HeroForm
    template_name = 'dashboardmanager/update/update_hero_section.html'
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'Hero section updated successfully'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_section'] = self.object
        return context
    
    def form_invalid(self, form):
        self.handle_form_errors(form)
        return super().form_invalid(form)

class FeatureUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """View for updating a feature"""
    model = Feature
    form_class = FeatureForm
    template_name = 'dashboardmanager/update/update_feature.html'
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'Feature updated successfully'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feature'] = self.object
        return context
    
    def form_invalid(self, form):
        self.handle_form_errors(form)
        return super().form_invalid(form)

class TestimonialUpdateView(AdminRequiredMixin, UpdateView):
    """View for updating a testimonial"""
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboardmanager/update/update_testimonial.html'
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'Testimonial updated successfully'
    
    def get_initial(self):
        """Set initial data for the form"""
        initial = super().get_initial()
        if self.object.image:
            initial['image'] = self.object.image
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonial'] = self.object
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Handle clear image checkbox
        if 'clear_image' in request.POST:
            self.object.image.delete()
            self.object.image = None
            self.object.save()
            messages.success(request, 'Image cleared successfully')
            return redirect('dashboardmanager:update_testimonial', pk=self.object.pk)
            
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Save the form first
        self.object = form.save()
        
        # Add success message
        messages.success(self.request, self.success_message)
        
        # Redirect to success URL
        return redirect(self.get_success_url())
        
    def form_invalid(self, form):
        # Log form errors for debugging
        print("Form errors:", form.errors)
        return super().form_invalid(form)

class HeroSectionDeleteView(DeleteView):
    """View for deleting a herosection"""
    model = HeroSection
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'Herosectionx deleted successfully'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
    
    def get(self, request, *args, **kwargs):
        # Only allow POST requests for deletion
        return redirect(self.success_url)

class FeatureDeleteView(DeleteView):
    """View for deleting a feature"""
    model = Feature
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'Feature deleted successfully'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
    
    def get(self, request, *args, **kwargs):
        # Only allow POST requests for deletion
        return redirect(self.success_url)

class TestimonialDeleteView(AdminRequiredMixin, DeleteView):
    """View for deleting a testimonial"""
    model = Testimonial
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'Testimonial deleted successfully'
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
    
    def get(self, request, *args, **kwargs):
        # Only allow POST requests for deletion
        return redirect(self.success_url)

class FAQUpdateView(AdminRequiredMixin, UpdateView):
    """View for updating an FAQ"""
    model = FAQ
    form_class = dashboardFAQForm
    template_name = 'dashboardmanager/update/update_faq.html'
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'FAQ updated successfully'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faq'] = self.object
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

class FAQDeleteView(AdminRequiredMixin, DeleteView):
    """View for deleting an FAQ"""
    model = FAQ
    success_url = reverse_lazy('dashboardmanager:landing_page')
    success_message = 'FAQ deleted successfully'

class BookmarkListView(LoginRequiredMixin, ListView):
    """View for listing and creating bookmarks"""
    model = DashboardBookmark
    template_name = 'dashboardmanager/bookmarks/list.html'
    context_object_name = 'bookmarks'
    
    def get_queryset(self):
        return DashboardBookmark.objects.filter(
            user=self.request.user
        ).order_by('-is_favorite', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BookmarkForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.user = request.user
            bookmark.save()
            messages.success(request, 'Bookmark added successfully')
            return redirect('dashboardmanager:bookmarks')
        
        # If form is invalid, re-render the page with errors
        return self.get(request, *args, **kwargs)

class BookmarkCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new bookmark"""
    model = DashboardBookmark
    form_class = BookmarkForm
    template_name = 'dashboardmanager/bookmarks/form.html'
    success_url = reverse_lazy('dashboardmanager:bookmarks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Bookmark'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Bookmark added successfully')
        return super().form_valid(form)

class BookmarkUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating an existing bookmark"""
    model = DashboardBookmark
    form_class = BookmarkForm
    template_name = 'dashboardmanager/bookmarks/form.html'
    success_url = reverse_lazy('dashboardmanager:bookmarks')
    
    def get_queryset(self):
        return DashboardBookmark.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Bookmark'
        context['bookmark'] = self.object
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Bookmark updated successfully')
        return super().form_valid(form)

class BookmarkDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a bookmark"""
    model = DashboardBookmark
    success_url = reverse_lazy('dashboardmanager:bookmarks')
    success_message = 'Bookmark deleted successfully'
    
    def get_queryset(self):
        return DashboardBookmark.objects.filter(user=self.request.user)

#note
class NoteListView(LoginRequiredMixin, ListView):
    """View for listing and creating notes"""
    model = DashboardNote
    template_name = 'dashboardmanager/notes/list.html'
    context_object_name = 'notes'
    
    def get_queryset(self):
        return DashboardNote.objects.filter(
            user=self.request.user
        ).order_by('-is_pinned', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NoteForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note added successfully')
            return redirect('dashboardmanager:notes')
        
        # If form is invalid, re-render the page with errors
        return self.get(request, *args, **kwargs)

class NoteCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new note"""
    model = DashboardNote
    form_class = NoteForm
    template_name = 'dashboardmanager/notes/form.html'
    success_url = reverse_lazy('dashboardmanager:notes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Note'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Note added successfully')
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating an existing note"""
    model = DashboardNote
    form_class = NoteForm
    template_name = 'dashboardmanager/notes/form.html'
    success_url = reverse_lazy('dashboardmanager:notes')
    
    def get_queryset(self):
        return DashboardNote.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Note'
        context['note'] = self.object
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Note updated successfully')
        return super().form_valid(form)

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a note"""
    model = DashboardNote
    success_url = reverse_lazy('dashboardmanager:notes')
    success_message = 'Note deleted successfully'
    
    def get_queryset(self):
        return DashboardNote.objects.filter(user=self.request.user)
    
#reminder
class ReminderListView(LoginRequiredMixin, ListView):
    """View for listing and creating reminders"""
    model = DashboardReminder
    template_name = 'dashboardmanager/reminders/list.html'
    context_object_name = 'reminders'
    
    def get_queryset(self):
        return DashboardReminder.objects.filter(
            user=self.request.user
        ).order_by('is_completed', 'due_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReminderForm()
        context['current_time'] = timezone.now()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, 'Reminder added successfully')
            return redirect('dashboardmanager:reminders')
        
        # If form is invalid, re-render the page with errors
        return self.get(request, *args, **kwargs)

class ReminderCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new reminder"""
    model = DashboardReminder
    form_class = ReminderForm
    template_name = 'dashboardmanager/reminders/form.html'
    success_url = reverse_lazy('dashboardmanager:reminders')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Reminder'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Reminder added successfully')
        return super().form_valid(form)

class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating an existing reminder"""
    model = DashboardReminder
    form_class = ReminderForm
    template_name = 'dashboardmanager/reminders/form.html'
    success_url = reverse_lazy('dashboardmanager:reminders')
    
    def get_queryset(self):
        return DashboardReminder.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Reminder'
        context['reminder'] = self.object
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Reminder updated successfully')
        return super().form_valid(form)

class ReminderDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a reminder"""
    model = DashboardReminder
    success_url = reverse_lazy('dashboardmanager:reminders')
    success_message = 'Reminder deleted successfully'
    
    def get_queryset(self):
        return DashboardReminder.objects.filter(user=self.request.user)

class ToggleReminderCompleteView(LoginRequiredMixin, View):
    """View for toggling reminder completion status"""
    def post(self, request, *args, **kwargs):
        reminder = get_object_or_404(DashboardReminder, pk=kwargs['pk'], user=request.user)
        reminder.is_completed = not reminder.is_completed
        reminder.save()
        status = 'completed' if reminder.is_completed else 'reopened'
        messages.success(request, f'Reminder {status} successfully')
        return redirect('dashboardmanager:reminders')

#shortcuts
class ShortcutListView(LoginRequiredMixin, ListView):
    """View for listing and creating shortcuts"""
    model = DashboardShortcut
    template_name = 'dashboardmanager/shortcuts/list.html'
    context_object_name = 'shortcuts'
    
    def get_queryset(self):
        return DashboardShortcut.objects.filter(
            user=self.request.user
        ).order_by('shortcut_key')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShortcutForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ShortcutForm(request.POST)
        if form.is_valid():
            shortcut = form.save(commit=False)
            shortcut.user = request.user
            shortcut.save()
            messages.success(request, 'Shortcut added successfully')
            return redirect('dashboardmanager:shortcuts')
        
        # If form is invalid, re-render the page with errors
        return self.get(request, *args, **kwargs)

class ShortcutCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new shortcut"""
    model = DashboardShortcut
    form_class = ShortcutForm
    template_name = 'dashboardmanager/shortcuts/form.html'
    success_url = reverse_lazy('dashboardmanager:shortcuts')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Shortcut'
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Shortcut added successfully')
        return super().form_valid(form)

class ShortcutUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating an existing shortcut"""
    model = DashboardShortcut
    form_class = ShortcutForm
    template_name = 'dashboardmanager/shortcuts/form.html'
    success_url = reverse_lazy('dashboardmanager:shortcuts')
    
    def get_queryset(self):
        return DashboardShortcut.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Shortcut'
        context['shortcut'] = self.object
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Shortcut updated successfully')
        return super().form_valid(form)

class ShortcutDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a shortcut"""
    model = DashboardShortcut
    success_url = reverse_lazy('dashboardmanager:shortcuts')
    success_message = 'Shortcut deleted successfully'
    
    def get_queryset(self):
        return DashboardShortcut.objects.filter(user=self.request.user)

class ToggleShortcutActiveView(LoginRequiredMixin, View):
    """View for toggling shortcut active status"""
    def post(self, request, **kwargs):
        shortcut = get_object_or_404(DashboardShortcut, pk=kwargs['pk'], user=request.user)
        shortcut.is_active = not shortcut.is_active
        shortcut.save()
        status = 'activated' if shortcut.is_active else 'deactivated'
        messages.success(request, f'Shortcut {status} successfully')
        return redirect('dashboardmanager:shortcuts')