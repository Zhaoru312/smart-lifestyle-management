from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.core.files.storage import default_storage
from django import forms
from .models import DashboardWidget, UserPreference, DashboardNotification, DashboardLayout , UserProfile
from landing.models import HeroSection, Feature, Testimonial, FAQ
import uuid

@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    # Get user preferences
    try:
        user_prefs = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        user_prefs = UserPreference.objects.create(user=request.user)
    
    # Get dashboard widgets
    widgets = DashboardWidget.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('position_y', 'position_x')
    
    # Get notifications
    notifications = DashboardNotification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    # Get dashboard statistics
    stats = {
        'total_expenses': 1234.56,  # Replace with actual data
        'workout_streak': 14,       # Replace with actual data
        'active_habits': 5,         # Replace with actual data
        'pending_tasks': 3          # Replace with actual data
    }

    # Get user's layouts
    layouts = DashboardLayout.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
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
        'widgets': widgets,
        'notifications': notifications,
        'user_prefs': user_prefs,
        'layouts': layouts
    }
    
    return render(request, 'dashboardmanager/index.html', context)

@login_required
def applist(request):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
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



# Add forms for each section

class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = ['title', 'subtitle', 'background_image', 'call_to_action_text', 'call_to_action_url', 'is_active']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['title', 'description', 'icon', 'order', 'is_active']

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'content', 'image', 'rating', 'is_active']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order', 'is_active']

class DashboardLayoutForm(forms.ModelForm):
    class Meta:
        model = DashboardLayout
        fields = ['name', 'description', 'layout_data', 'is_default', 'is_public']

@login_required
def list_layouts(request):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    # Get all layouts for the user
    layouts = DashboardLayout.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    context = {
        'user': request.user,
        'layouts': layouts
    }
    
    return render(request, 'dashboardmanager/layouts/list.html', context)

@login_required
def create_layout(request):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    if request.method == 'POST':
        form = DashboardLayoutForm(request.POST)
        if form.is_valid():
            layout = form.save(commit=False)
            layout.user = request.user
            layout.save()
            messages.success(request, 'Layout created successfully')
            return redirect('dashboardmanager:list_layouts')
    else:
        form = DashboardLayoutForm()
    
    context = {
        'user': request.user,
        'form': form
    }
    
    return render(request, 'dashboardmanager/layouts/create.html', context)

@login_required
def view_layout(request, pk):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    layout = get_object_or_404(DashboardLayout, pk=pk, user=request.user)
    
    context = {
        'user': request.user,
        'layout': layout
    }
    
    return render(request, 'dashboardmanager/layouts/view.html', context)

@login_required
def edit_layout(request, pk):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    layout = get_object_or_404(DashboardLayout, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DashboardLayoutForm(request.POST, instance=layout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Layout updated successfully')
            return redirect('dashboardmanager:view_layout', pk=pk)
    else:
        form = DashboardLayoutForm(instance=layout)
    
    context = {
        'user': request.user,
        'layout': layout,
        'form': form
    }
    
    return render(request, 'dashboardmanager/layouts/edit.html', context)

@login_required
def delete_layout(request, pk):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    layout = get_object_or_404(DashboardLayout, pk=pk, user=request.user)
    
    if request.method == 'POST':
        layout.delete()
        messages.success(request, 'Layout deleted successfully')
        return redirect('dashboardmanager:list_layouts')
    
    context = {
        'user': request.user,
        'layout': layout
    }
    
    return render(request, 'dashboardmanager/layouts/delete.html', context)

@login_required
def set_default_layout(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        layout = get_object_or_404(DashboardLayout, pk=pk, user=request.user)
        layout.is_default = True
        layout.save()
        
        # Ensure only one layout per user can be default
        DashboardLayout.objects.filter(
            user=request.user,
            is_default=True
        ).exclude(pk=pk).update(is_default=False)
        
        return JsonResponse({
            'success': True,
            'message': 'Default layout set successfully'
        })
    except DashboardLayout.DoesNotExist:
        return JsonResponse({'error': 'Layout not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Handle avatar upload
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            if avatar.size > 5 * 1024 * 1024:  # 5MB limit
                messages.error(request, 'Avatar file size must be less than 5MB')
                return redirect('dashboardmanager:profile')
            else:
                # Delete old avatar if exists
                if profile.avatar:
                    try:
                        default_storage.delete(profile.avatar.path)
                    except:
                        pass

                # Save new avatar
                filename = f"profile_avatars/{request.user.username}_{uuid.uuid4()}.jpg"
                with default_storage.open(filename, 'wb') as destination:
                    for chunk in avatar.chunks():
                        destination.write(chunk)
                profile.avatar = filename

        # Handle profile fields with validation
        errors = {}
        
        # Validate birth date
        birth_date = request.POST.get('birth_date')
        if birth_date:
            try:
                birth_date = timezone.datetime.strptime(birth_date, '%Y-%m-%d').date()
                if birth_date > timezone.now().date():
                    errors['birth_date'] = 'Birth date cannot be in the future'
            except ValueError:
                errors['birth_date'] = 'Invalid date format. Please use YYYY-MM-DD'
        
        # Validate phone number
        phone_number = request.POST.get('phone_number', '')
        if phone_number:
            if not phone_number.isdigit():
                errors['phone_number'] = 'Phone number can only contain digits'
            if len(phone_number) < 8 or len(phone_number) > 15:
                errors['phone_number'] = 'Phone number must be between 8 and 15 digits'
        
        # Validate website URL
        website = request.POST.get('website', '')
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        # Update profile fields
        profile.bio = request.POST.get('bio', '')
        profile.birth_date = birth_date if not errors.get('birth_date') else None
        profile.phone_number = phone_number if not errors.get('phone_number') else ''
        profile.address = request.POST.get('address', '')
        profile.website = website
        profile.interests = request.POST.get('interests', '')
        profile.profession = request.POST.get('profession', '')
        profile.company = request.POST.get('company', '')
        profile.location = request.POST.get('location', '')

        # Handle social media
        social_media = {}
        for platform in ['facebook', 'twitter', 'linkedin', 'instagram']:
            url = request.POST.get(f'social_media[{platform}]', '')
            if url:
                social_media[platform] = url
        profile.social_media = social_media

        # Handle notification preferences
        profile.notification_email = request.POST.get('notification_email') == 'on'
        profile.notification_sms = request.POST.get('notification_sms') == 'on'
        profile.notification_push = request.POST.get('notification_push') == 'on'

        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('dashboardmanager:profile')

    # Get user's default layout
    default_layout = DashboardLayout.objects.filter(user=request.user, is_default=True).first()
    
    # Handle layout setting
    if request.method == 'POST' and 'layout_id' in request.POST:
        try:
            layout_id = request.POST.get('layout_id')
            if layout_id:
                layout = DashboardLayout.objects.get(pk=layout_id, user=request.user)
                layout.is_default = True
                layout.save()
                messages.success(request, 'Default layout set successfully')
            else:
                messages.error(request, 'Please select a layout')
        except DashboardLayout.DoesNotExist:
            messages.error(request, 'Layout not found')
        except Exception as e:
            messages.error(request, f'Error setting layout: {str(e)}')
        
        return redirect('dashboardmanager:profile')

    return render(request, 'dashboardmanager/profile.html', {
        'profile': profile,
        'default_layout': default_layout,
        'layouts': DashboardLayout.objects.filter(user=request.user)
    })

@login_required
def landing_page(request):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    # Handle form submissions
    if request.method == 'POST':
        if 'add_hero' in request.POST:
            hero_form = HeroSectionForm(request.POST, request.FILES)
            if hero_form.is_valid():
                hero_form.save()
                messages.success(request, 'Hero section added successfully')
                return redirect('dashboardmanager:landing_page')
        elif 'add_feature' in request.POST:
            feature_form = FeatureForm(request.POST)
            if feature_form.is_valid():
                feature_form.save()
                messages.success(request, 'Feature added successfully')
                return redirect('dashboardmanager:landing_page')
        elif 'add_testimonial' in request.POST:
            testimonial_form = TestimonialForm(request.POST, request.FILES)
            if testimonial_form.is_valid():
                testimonial_form.save()
                messages.success(request, 'Testimonial added successfully')
                return redirect('dashboardmanager:landing_page')
        elif 'add_faq' in request.POST:
            faq_form = FAQForm(request.POST)
            if faq_form.is_valid():
                faq_form.save()
                messages.success(request, 'FAQ added successfully')
                return redirect('dashboardmanager:landing_page')
    
    # Get all data
    hero_sections = HeroSection.objects.all()
    features = Feature.objects.all()
    testimonials = Testimonial.objects.all()
    faqs = FAQ.objects.all()
    
    # Initialize empty forms
    hero_form = HeroSectionForm()
    feature_form = FeatureForm()
    testimonial_form = TestimonialForm()
    faq_form = FAQForm()
    
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
    
    hero_section = HeroSection.objects.get(pk=pk)
    
    if request.method == 'POST':
        hero_section.title = request.POST.get('title')
        hero_section.subtitle = request.POST.get('subtitle')
        hero_section.call_to_action_text = request.POST.get('call_to_action_text')
        hero_section.call_to_action_url = request.POST.get('call_to_action_url')
        hero_section.is_active = request.POST.get('is_active') == 'on'
        
        if 'background_image' in request.FILES:
            hero_section.background_image = request.FILES['background_image']
        
        hero_section.save()
        messages.success(request, 'Hero section updated successfully')
        return redirect('dashboardmanager:landing_page')
    
    context = {'hero_section': hero_section}
    return render(request, 'dashboardmanager/update_hero_section.html', context)

@login_required
def update_feature(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    feature = Feature.objects.get(pk=pk)
    
    if request.method == 'POST':
        feature.title = request.POST.get('title')
        feature.description = request.POST.get('description')
        feature.icon = request.POST.get('icon')
        feature.order = int(request.POST.get('order'))
        feature.is_active = request.POST.get('is_active') == 'on'
        feature.save()
        messages.success(request, 'Feature updated successfully')
        return redirect('dashboardmanager:landing_page')
    
    context = {'feature': feature}
    return render(request, 'dashboardmanager/update_feature.html', context)

@login_required
def update_testimonial(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    testimonial = Testimonial.objects.get(pk=pk)
    
    if request.method == 'POST':
        testimonial.name = request.POST.get('name')
        testimonial.role = request.POST.get('role')
        testimonial.content = request.POST.get('content')
        testimonial.rating = int(request.POST.get('rating'))
        testimonial.is_active = request.POST.get('is_active') == 'on'
        
        if 'image' in request.FILES:
            testimonial.image = request.FILES['image']
        
        testimonial.save()
        messages.success(request, 'Testimonial updated successfully')
        return redirect('dashboardmanager:landing_page')
    
    context = {'testimonial': testimonial}
    return render(request, 'dashboardmanager/update_testimonial.html', context)

@login_required
def update_faq(request, pk):
    if not request.user.is_superuser:
        return redirect('dashboardmanager:index')
    
    faq = FAQ.objects.get(pk=pk)
    
    if request.method == 'POST':
        faq.question = request.POST.get('question')
        faq.answer = request.POST.get('answer')
        faq.category = request.POST.get('category')
        faq.order = int(request.POST.get('order'))
        faq.is_active = request.POST.get('is_active') == 'on'
        faq.save()
        messages.success(request, 'FAQ updated successfully')
        return redirect('dashboardmanager:landing_page')
    
    context = {'faq': faq}
    return render(request, 'dashboardmanager/update_faq.html', context)