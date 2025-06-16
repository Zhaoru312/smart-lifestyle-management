# Django imports
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import View, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.utils import timezone
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Avg, Count, Q, Sum, F
import uuid
from datetime import date

# Import models from other apps
from taskmanager.models import Task, TaskActivity
from mealtracker.models import Meal, Drink, DietType, AvoidItem, Supplement
from financialmanagement.models import Expense, Income, FinancialGoal, Budget
from fitnesstracker.models import BodyStat, ActivityLog, FitnessGoal, Exercise

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
        user = self.request.user
        
        # Initialize stats dictionary
        stats = {
            'pending_tasks': 0,
            'completed_tasks': 0,
            'total_projects': 0,
            'meals_today': 0,
            'calories_today': 0,
            'total_meals': 0
        }
        
        # Get task manager stats
        task_stats = Task.objects.filter(user=user).aggregate(
            pending=Count('id', filter=Q(is_completed=False)),
            completed=Count('id', filter=Q(is_completed=True)),
            total_projects=Count('project', distinct=True)
        )
        stats.update({
            'pending_tasks': task_stats['pending'] or 0,
            'completed_tasks': task_stats['completed'] or 0,
            'total_projects': task_stats['total_projects'] or 0
        })
        
        # Get upcoming tasks
        upcoming_tasks = Task.objects.filter(
            user=user,
            is_completed=False,
            deadline__gte=date.today()
        ).order_by('deadline')[:5]
        
        context['upcoming_tasks'] = upcoming_tasks
        
        # Get meal stats
        total_meals = Meal.objects.count()
        total_drinks = Drink.objects.count()
        avg_calories = Meal.objects.aggregate(avg=Avg('calories'))['avg'] or 0
        
        # Get financial stats
        current_month = timezone.now().month
        current_year = timezone.now().year
        
        # Calculate monthly income
        monthly_income = Income.objects.filter(
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate monthly expenses
        monthly_expenses = Expense.objects.filter(
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Calculate savings rate (income - expenses) / income * 100
        savings_rate = 0
        if monthly_income > 0:
            savings_rate = ((monthly_income - monthly_expenses) / monthly_income) * 100
            savings_rate = round(savings_rate, 2)
        
        # Get fitness stats
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        end_of_week = start_of_week + timezone.timedelta(days=6)
        
        # Count workouts this week (without user filter since ActivityLog doesn't have a user field)
        workouts_this_week = ActivityLog.objects.filter(
            date__range=[start_of_week, end_of_week]
        ).count()
        
        # Get active fitness goals (without user filter since FitnessGoal doesn't have a user field)
        fitness_goals = FitnessGoal.objects.filter(
            is_achieved=False
        ).order_by('-id')[:3]  # Show 3 most recent goals
        
        # Update stats with all data
        stats.update({
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'savings_rate': savings_rate,
            'workouts_this_week': workouts_this_week,
        })
        
        stats.update({
            'total_meals': total_meals,
            'total_drinks': total_drinks,
            'avg_meal_calories': round(avg_calories, 1),
            'total_diets': DietType.objects.count(),
            'total_supplements': Supplement.objects.count()
        })
        
        # Get recent meals and drinks
        context.update({
            'recent_meals': Meal.objects.select_related('category').order_by('-id')[:5],
            'recent_drinks': Drink.objects.select_related('category').order_by('-id')[:5],
            'diet_types': DietType.objects.all()[:3],
            'avoid_items': AvoidItem.objects.order_by('-severity')[:3],
            'supplements': Supplement.objects.all()[:3]
        })
        
        # Get financial data
        today = timezone.now().date()
        month_start = today.replace(day=1)
        
        # Calculate monthly income and expenses
        monthly_expenses = Expense.objects.filter(
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_income = Income.objects.filter(
            date__year=month_start.year,
            date__month=month_start.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Get recent transactions
        recent_expenses = Expense.objects.select_related('category').order_by('-date')[:5]
        recent_incomes = Income.objects.select_related('category').order_by('-date')[:5]
        
        # Get financial goals
        active_goals = FinancialGoal.objects.filter(
            due_date__gte=today
        ).order_by('due_date')[:3]
        
        # Update stats with financial data
        stats.update({
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'savings_rate': round(((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0, 1),
            'active_goals_count': FinancialGoal.objects.filter(due_date__gte=today).count(),
        })
        
        # Get fitness data
        latest_body_stat = BodyStat.objects.order_by('-date').first()
        recent_workouts = ActivityLog.objects.order_by('-date')[:5]
        fitness_goals = FitnessGoal.objects.filter(is_achieved=False).order_by('target_date')[:3]
        
        # Update stats with fitness data
        if latest_body_stat:
            stats.update({
                'current_weight': latest_body_stat.weight_kg,
                'body_fat': latest_body_stat.body_fat_percentage,
                'workouts_this_week': ActivityLog.objects.filter(
                    date__gte=today - timezone.timedelta(days=7)
                ).count(),
                'active_goals': FitnessGoal.objects.filter(is_achieved=False).count(),
            })
        
        # Get user's dashboard items
        context.update({
            'stats': stats,
            'recent_activity': self._get_recent_activity(),
            'fitness_goals': fitness_goals,
            'bookmarks': DashboardBookmark.objects.filter(user=user).order_by('-is_favorite', '-created_at')[:3],
            'notes': DashboardNote.objects.filter(user=user).order_by('-is_pinned', '-created_at')[:3],
            'reminders': DashboardReminder.objects.filter(user=user).order_by('is_completed', 'due_date')[:3],
            'shortcuts': DashboardShortcut.objects.filter(user=user, is_active=True).order_by('shortcut_key')[:3],
            # Financial data
            'recent_expenses': recent_expenses,
            'recent_incomes': recent_incomes,
            'active_goals': active_goals,
            'current_budget': Budget.objects.order_by('-end_date').first(),
            # Fitness data
            'latest_body_stat': latest_body_stat,
            'recent_workouts': recent_workouts,
            'fitness_goals': fitness_goals,
        })
        return context
    
    def _get_recent_activity(self):
        """Helper method to get recent activity across all apps"""
        activities = []
        user = self.request.user
        today = timezone.now().date()
        
        # Get recent task activities
        task_activities = TaskActivity.objects.filter(
            task__user=user
        ).select_related('task').order_by('-created_at')[:5]
        
        for activity in task_activities:
            activities.append({
                'date': activity.created_at.strftime('%Y-%m-%d'),
                'time': activity.created_at.strftime('%H:%M'),
                'activity': f"{activity.get_activity_type_display()} task: {activity.task.title if activity.task else 'N/A'}",
                'category': 'Task',
                'status': 'completed' if activity.activity_type == 'complete' else 'updated',
                'icon': 'fa-tasks',
                'color': 'primary'
            })
            
        # Add financial activities
        recent_expenses = Expense.objects.order_by('-date')[:3]
        for expense in recent_expenses:
            activities.append({
                'date': expense.date.strftime('%Y-%m-%d'),
                'time': expense.created_at.strftime('%H:%M') if expense.created_at else '00:00',
                'activity': f"Expense: {expense.name} - ${expense.amount}",
                'category': 'Finance',
                'status': 'expense',
                'icon': 'fa-arrow-down',
                'color': 'danger'
            })
            
        recent_incomes = Income.objects.order_by('-date')[:2]
        for income in recent_incomes:
            activities.append({
                'date': income.date.strftime('%Y-%m-%d'),
                'time': income.created_at.strftime('%H:%M') if income.created_at else '00:00',
                'activity': f"Income: {income.name} - ${income.amount}",
                'category': 'Finance',
                'status': 'income',
                'icon': 'fa-arrow-up',
                'color': 'success'
            })
            
        # Add fitness activities
        recent_workouts = ActivityLog.objects.order_by('-date')[:3]
        for workout in recent_workouts:
            activities.append({
                'date': workout.date.strftime('%Y-%m-%d'),
                'time': 'Workout',
                'activity': f"{workout.activity_type} for {workout.duration_minutes} mins",
                'category': 'Fitness',
                'status': 'completed',
                'icon': 'fa-dumbbell',
                'color': 'info'
            })
    
        # Add recent meal and drink activities
        recent_meals = Meal.objects.order_by('-id')[:3]
        recent_drinks = Drink.objects.order_by('-id')[:2]
        
        for meal in recent_meals:
            activities.append({
                'date': timezone.now().strftime('%Y-%m-%d'),
                'time': timezone.now().strftime('%H:%M'),
                'activity': f"Meal: {meal.name} ({meal.calories} cal)",
                'category': 'Meal',
                'status': 'completed'
            })
            
        for drink in recent_drinks:
            activities.append({
                'date': timezone.now().strftime('%Y-%m-%d'),
                'time': timezone.now().strftime('%H:%M'),
                'activity': f"Drink: {drink.name} ({drink.calories} cal)",
                'category': 'Drink',
                'status': 'completed'
            })
        
        # Sort all activities by date and time (newest first)
        activities.sort(key=lambda x: (x['date'], x['time']), reverse=True)
        
        # Return only the 5 most recent activities
        return activities[:5]

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