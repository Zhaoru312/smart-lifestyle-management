from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from landing.models import HeroSection, Feature, Testimonial, FAQ

@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('landing:login')
    
    apps = [
        {'name': 'Finance', 'url': '/finance/', 'icon': 'fas fa-wallet'},
        {'name': 'Fitness', 'url': '/fitness/', 'icon': 'fas fa-dumbbell'},
        {'name': 'Habit', 'url': '/habit/', 'icon': 'fas fa-repeat'},
        {'name': 'Meal', 'url': '/meal/', 'icon': 'fas fa-utensils'},
        {'name': 'Mental', 'url': '/mental/', 'icon': 'fas fa-brain'},
        {'name': 'Tasks', 'url': '/tasks/', 'icon': 'fas fa-tasks'}
    ]
    
    if request.user.is_superuser:
        apps.append({'name': 'Landing Page', 'url': '/dashboard/landing/', 'icon': 'fas fa-home'})
    
    context = {
        'user': request.user,
        'apps': apps
    }
    
    return render(request, 'dashboardmanager/index.html', context)

from django import forms

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
        fields = ['question', 'answer', 'category', 'order', 'is_active']

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