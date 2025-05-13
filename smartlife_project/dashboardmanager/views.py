# Standard library imports
import uuid

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.utils import timezone

# Local application imports
from .models import UserProfile, DashboardBookmark, DashboardNote, DashboardReminder, DashboardShortcut
from landing.models import HeroSection, Feature, Testimonial, FAQ
from .forms import (
    ProfileForm, HeroForm, FeatureForm, TestimonialForm, FAQForm,
    BookmarkForm, NoteForm, ReminderForm, ShortcutForm
)

# Helper functions for common operations
def handle_form_errors(form, request):
    """Display form errors as messages"""
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f"{field}: {error}")

def process_form(request, form_class, instance=None, success_url=None, success_message=None):
    """Generic function to handle form processing"""
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            if not instance:  # Creating a new object
                obj.user = request.user
            obj.save()
            if success_message:
                messages.success(request, success_message)
            return redirect(success_url)
        else:
            handle_form_errors(form, request)
    else:
        form = form_class(instance=instance)
    return form

@login_required
def index(request):
    
    # Get dashboard statistics
    stats = {
        'total_expenses': 1234.56,  # Replace with actual data
        'workout_streak': 14,       # Replace with actual data
        'active_habits': 5,         # Replace with actual data
        'pending_tasks': 3          # Replace with actual data
    }
    
    # Get user's dashboard items
    bookmarks = DashboardBookmark.objects.filter(user=request.user).order_by('-is_favorite', '-created_at')[:3]
    notes = DashboardNote.objects.filter(user=request.user).order_by('-is_pinned', '-created_at')[:3]
    reminders = DashboardReminder.objects.filter(user=request.user).order_by('is_completed', 'due_date')[:3]
    shortcuts = DashboardShortcut.objects.filter(user=request.user, is_active=True).order_by('shortcut_key')[:3]
    
    # Get recent activity
    recent_activity = [
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
    
    context = {
        'user': request.user,
        'stats': stats,
        'recent_activity': recent_activity,
        'bookmarks': bookmarks,
        'notes': notes,
        'reminders': reminders,
        'shortcuts': shortcuts,
    }
    
    return render(request, 'dashboardmanager/index.html', context)

@login_required
def applist(request):
    
    apps = [
        {'name': 'Finance', 'url': '/finance/', 'icon': 'fas fa-wallet', 'description': 'Manage your finances and track expenses'},
        {'name': 'Fitness', 'url': '/fitness/', 'icon': 'fas fa-dumbbell', 'description': 'Track your workouts and fitness goals'},
        {'name': 'Habit', 'url': '/habit/', 'icon': 'fas fa-check-circle', 'description': 'Build and track your habits'},
        {'name': 'Meal', 'url': '/meal/', 'icon': 'fas fa-utensils', 'description': 'Log and plan your meals'},
        {'name': 'Mental', 'url': '/mental/', 'icon': 'fas fa-brain', 'description': 'Track your mental health and mood'},
        {'name': 'Tasks', 'url': '/tasks/', 'icon': 'fas fa-tasks', 'description': 'Manage your daily tasks and to-do list'}
    ]
    
    if request.user.is_superuser:
        apps.append({
            'name': 'Landing Page', 
            'url': '/dashboard/landing/', 
            'icon': 'fas fa-home',
            'description': 'Manage the landing page content'
        })
    
    context = {
        'user': request.user,
        'apps': apps
    }
    
    return render(request, 'dashboardmanager/applist.html', context)

# Additional imports

@login_required
def profile(request):
    
    # Get or create user profile
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    # Initialize form
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Handle avatar upload
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                # Delete old avatar if exists
                if profile.avatar:
                    try:
                        default_storage.delete(profile.avatar.path)
                    except:
                        pass

                # Save new avatar with unique filename
                filename = f"profile_avatars/{request.user.username}_{uuid.uuid4()}.jpg"
                with default_storage.open(filename, 'wb') as destination:
                    for chunk in avatar.chunks():
                        destination.write(chunk)
                profile.avatar = filename

            # Handle social media updates if provided
            if 'social_media_platform' in request.POST and 'social_media_url' in request.POST:
                platform = request.POST.get('social_media_platform')
                url = request.POST.get('social_media_url')
                if platform and url:
                    social_media = profile.social_media or {}
                    social_media[platform] = url
                    profile.social_media = social_media

            # Save the form
            profile = form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboardmanager:profile')
        else:
            # Form is invalid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    # Get today's date for max date in birth_date field
    today = timezone.now().date()
    
    return render(request, 'dashboardmanager/profile.html', {
        'profile': profile,
        'form': form,
        'today': today,
    })

@login_required
def landing_page(request):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    # Get all data
    hero_sections = HeroSection.objects.all().order_by('-is_active', 'id')
    features = Feature.objects.all().order_by('order', '-is_active')
    testimonials = Testimonial.objects.all().order_by('-is_active', 'id')
    faqs = FAQ.objects.all().order_by('order', '-is_active')
    
    # Initialize forms
    hero_form = HeroForm(request.POST or None, request.FILES or None)
    feature_form = FeatureForm(request.POST or None)
    testimonial_form = TestimonialForm(request.POST or None, request.FILES or None)
    faq_form = FAQForm(request.POST or None)
    
    # Handle form submissions
    if request.method == 'POST':
        # Hero Section
        if 'add_hero' in request.POST:
            if hero_form.is_valid():
                hero = hero_form.save(commit=False)
                if not hero.call_to_action_url:
                    hero.call_to_action_url = None
                hero.save()
                messages.success(request, 'Hero section added successfully')
                hero_form = HeroForm()  # Reset form after successful submission
            else:
                messages.error(request, 'Please fix the errors below')
                
        # Feature
        elif 'add_feature' in request.POST:
            if feature_form.is_valid():
                feature_form.save()
                messages.success(request, 'Feature added successfully')
                feature_form = FeatureForm()  # Reset form after successful submission
            else:
                messages.error(request, 'Please fix the errors below')
                
        # Testimonial
        elif 'add_testimonial' in request.POST:
            if testimonial_form.is_valid():
                testimonial_form.save()
                messages.success(request, 'Testimonial added successfully')
                testimonial_form = TestimonialForm()  # Reset form after successful submission
            else:
                messages.error(request, 'Please fix the errors below')
                
        # FAQ
        elif 'add_faq' in request.POST:
            if faq_form.is_valid():
                faq_form.save()
                messages.success(request, 'FAQ added successfully')
                faq_form = FAQForm()  # Reset form after successful submission
            else:
                messages.error(request, 'Please fix the errors below')
    
    context = {
        'hero_sections': hero_sections,
        'features': features,
        'testimonials': testimonials,
        'faqs': faqs,
        'hero_form': hero_form,
        'feature_form': feature_form,
        'testimonial_form': testimonial_form,
        'faq_form': faq_form
    }
    
    return render(request, 'dashboardmanager/landing_page.html', context)

@login_required
def update_hero_section(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    hero_section = get_object_or_404(HeroSection, pk=pk)
    
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES, instance=hero_section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hero section updated successfully')
            return redirect('dashboardmanager:landing_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = HeroForm(instance=hero_section)
    
    context = {
        'hero_section': hero_section,
        'form': form
    }
    return render(request, 'dashboardmanager/update_hero_section.html', context)

@login_required
def update_feature(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    feature = get_object_or_404(Feature, pk=pk)
    
    if request.method == 'POST':
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature updated successfully')
            return redirect('dashboardmanager:landing_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FeatureForm(instance=feature)
    
    context = {
        'feature': feature,
        'form': form
    }
    return render(request, 'dashboardmanager/update_feature.html', context)

@login_required
def update_testimonial(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    testimonial = get_object_or_404(Testimonial, pk=pk)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully')
            return redirect('dashboardmanager:landing_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TestimonialForm(instance=testimonial)
    
    context = {
        'testimonial': testimonial,
        'form': form
    }
    return render(request, 'dashboardmanager/update_testimonial.html', context)

@login_required
def update_faq(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    faq = get_object_or_404(FAQ, pk=pk)
    
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ updated successfully')
            return redirect('dashboardmanager:landing_page')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FAQForm(instance=faq)
    
    context = {
        'faq': faq,
        'form': form
    }
    return render(request, 'dashboardmanager/update_faq.html', context)

@login_required
def delete_hero_section(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    hero = get_object_or_404(HeroSection, pk=pk)
    if request.method == 'POST':
        hero.delete()
        messages.success(request, 'Hero section deleted successfully')
        return redirect('dashboardmanager:landing_page')
    return redirect('dashboardmanager:landing_page')

@login_required
def delete_feature(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        feature.delete()
        messages.success(request, 'Feature deleted successfully')
        return redirect('dashboardmanager:landing_page')
    return redirect('dashboardmanager:landing_page')

@login_required
def delete_testimonial(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully')
        return redirect('dashboardmanager:landing_page')
    return redirect('dashboardmanager:landing_page')

@login_required
def delete_faq(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, 'FAQ deleted successfully')
    return redirect('dashboardmanager:landing_page')


# Bookmark Views
@login_required
def bookmark_list(request):
    bookmarks = DashboardBookmark.objects.filter(user=request.user).order_by('-is_favorite', '-created_at')
    return render(request, 'dashboardmanager/bookmarks/list.html', {
        'bookmarks': bookmarks
    })

@login_required
def add_bookmark(request):
    form = process_form(
        request=request,
        form_class=BookmarkForm,
        success_url='dashboardmanager:bookmark_list',
        success_message='Bookmark added successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/bookmarks/form.html', {
        'form': form,
        'title': 'Add Bookmark'
    })

@login_required
def edit_bookmark(request, pk):
    bookmark = get_object_or_404(DashboardBookmark, pk=pk, user=request.user)
    
    form = process_form(
        request=request,
        form_class=BookmarkForm,
        instance=bookmark,
        success_url='dashboardmanager:bookmark_list',
        success_message='Bookmark updated successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/bookmarks/form.html', {
        'form': form,
        'bookmark': bookmark,
        'title': 'Edit Bookmark'
    })

@login_required
def delete_bookmark(request, pk):
    bookmark = get_object_or_404(DashboardBookmark, pk=pk, user=request.user)
    bookmark.delete()
    messages.success(request, 'Bookmark deleted successfully')
    return redirect('dashboardmanager:bookmark_list')


# Note Views
@login_required
def note_list(request):
    notes = DashboardNote.objects.filter(user=request.user).order_by('-is_pinned', '-created_at')
    return render(request, 'dashboardmanager/notes/list.html', {
        'notes': notes
    })

@login_required
def add_note(request):
    form = process_form(
        request=request,
        form_class=NoteForm,
        success_url='dashboardmanager:note_list',
        success_message='Note added successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/notes/form.html', {
        'form': form,
        'title': 'Add Note'
    })

@login_required
def edit_note(request, pk):
    note = get_object_or_404(DashboardNote, pk=pk, user=request.user)
    
    form = process_form(
        request=request,
        form_class=NoteForm,
        instance=note,
        success_url='dashboardmanager:note_list',
        success_message='Note updated successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/notes/form.html', {
        'form': form,
        'note': note,
        'title': 'Edit Note'
    })

@login_required
def delete_note(request, pk):
    note = get_object_or_404(DashboardNote, pk=pk, user=request.user)
    note.delete()
    messages.success(request, 'Note deleted successfully')
    return redirect('dashboardmanager:note_list')


# Reminder Views
@login_required
def reminder_list(request):
    reminders = DashboardReminder.objects.filter(user=request.user).order_by('is_completed', 'due_date')
    return render(request, 'dashboardmanager/reminders/list.html', {
        'reminders': reminders
    })

@login_required
def add_reminder(request):
    form = process_form(
        request=request,
        form_class=ReminderForm,
        success_url='dashboardmanager:reminder_list',
        success_message='Reminder added successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/reminders/form.html', {
        'form': form,
        'title': 'Add Reminder'
    })

@login_required
def edit_reminder(request, pk):
    reminder = get_object_or_404(DashboardReminder, pk=pk, user=request.user)
    
    form = process_form(
        request=request,
        form_class=ReminderForm,
        instance=reminder,
        success_url='dashboardmanager:reminder_list',
        success_message='Reminder updated successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/reminders/form.html', {
        'form': form,
        'reminder': reminder,
        'title': 'Edit Reminder'
    })

@login_required
def delete_reminder(request, pk):
    reminder = get_object_or_404(DashboardReminder, pk=pk, user=request.user)
    reminder.delete()
    messages.success(request, 'Reminder deleted successfully')
    return redirect('dashboardmanager:reminder_list')

@login_required
def toggle_reminder_complete(request, pk):
    reminder = get_object_or_404(DashboardReminder, pk=pk, user=request.user)
    reminder.is_completed = not reminder.is_completed
    reminder.save()
    status = 'completed' if reminder.is_completed else 'reopened'
    messages.success(request, f'Reminder {status} successfully')
    return redirect('dashboardmanager:reminder_list')


# Shortcut Views
@login_required
def shortcut_list(request):
    shortcuts = DashboardShortcut.objects.filter(user=request.user).order_by('shortcut_key')
    return render(request, 'dashboardmanager/shortcuts/list.html', {
        'shortcuts': shortcuts
    })

@login_required
def add_shortcut(request):
    form = process_form(
        request=request,
        form_class=ShortcutForm,
        success_url='dashboardmanager:shortcut_list',
        success_message='Shortcut added successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/shortcuts/form.html', {
        'form': form,
        'title': 'Add Shortcut'
    })

@login_required
def edit_shortcut(request, pk):
    shortcut = get_object_or_404(DashboardShortcut, pk=pk, user=request.user)
    
    form = process_form(
        request=request,
        form_class=ShortcutForm,
        instance=shortcut,
        success_url='dashboardmanager:shortcut_list',
        success_message='Shortcut updated successfully'
    )
    
    # If form processing returned a redirect response, return it
    if isinstance(form, (redirect, JsonResponse)):
        return form
    
    return render(request, 'dashboardmanager/shortcuts/form.html', {
        'form': form,
        'shortcut': shortcut,
        'title': 'Edit Shortcut'
    })

@login_required
def delete_shortcut(request, pk):
    shortcut = get_object_or_404(DashboardShortcut, pk=pk, user=request.user)
    shortcut.delete()
    messages.success(request, 'Shortcut deleted successfully')
    return redirect('dashboardmanager:shortcut_list')

@login_required
def toggle_shortcut_active(request, pk):
    shortcut = get_object_or_404(DashboardShortcut, pk=pk, user=request.user)
    shortcut.is_active = not shortcut.is_active
    shortcut.save()
    status = 'activated' if shortcut.is_active else 'deactivated'
    messages.success(request, f'Shortcut {status} successfully')
    return redirect('dashboardmanager:shortcut_list')