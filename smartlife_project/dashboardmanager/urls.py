from django.urls import path
from .views import (
    DashboardView, AppListView, ProfileView, LandingPageView,
    HeroSectionUpdateView, FeatureUpdateView, TestimonialUpdateView, FAQUpdateView,
    HeroSectionDeleteView, FeatureDeleteView, TestimonialDeleteView, FAQDeleteView, BookmarkListView, BookmarkCreateView,
    BookmarkUpdateView, BookmarkDeleteView, NoteListView, NoteCreateView,
    NoteUpdateView, NoteDeleteView, ReminderListView, ReminderCreateView,
    ReminderUpdateView, ReminderDeleteView, ToggleReminderCompleteView,
    ShortcutListView, ShortcutCreateView, ShortcutUpdateView, ShortcutDeleteView,
    ToggleShortcutActiveView
)

app_name = 'dashboardmanager'

urlpatterns = [
    # Dashboard main views
    path('', DashboardView.as_view(), name='index'),
    path('applist/', AppListView.as_view(), name='applist'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Landing page management
    path('landing/', LandingPageView.as_view(), name='landing_page'),
    path('landing/hero/<int:pk>/', HeroSectionUpdateView.as_view(), name='update_hero_section'),
    path('landing/feature/<int:pk>/', FeatureUpdateView.as_view(), name='update_feature'),
    path('landing/testimonial/<int:pk>/', TestimonialUpdateView.as_view(), name='update_testimonial'),
    path('landing/faq/<int:pk>/', FAQUpdateView.as_view(), name='update_faq'),
    path('landing/testimonial/<int:pk>/delete/', TestimonialDeleteView.as_view(), name='delete_testimonial'),
    path('landing/faq/<int:pk>/delete/', FAQDeleteView.as_view(), name='delete_faq'),
    path('landing/hero/<int:pk>/delete/', HeroSectionDeleteView.as_view(), name='delete_hero_section'),
    path('landing/feature/<int:pk>/delete/', FeatureDeleteView.as_view(), name='delete_feature'),
    
    # Bookmark management
    path('bookmarks/', BookmarkListView.as_view(), name='bookmarks'),
    path('bookmarks/add/', BookmarkCreateView.as_view(), name='add_bookmark'),
    path('bookmarks/<int:pk>/edit/', BookmarkUpdateView.as_view(), name='edit_bookmark'),
    path('bookmarks/<int:pk>/delete/', BookmarkDeleteView.as_view(), name='delete_bookmark'),
    
    # Note management
    path('notes/', NoteListView.as_view(), name='notes'),
    path('notes/add/', NoteCreateView.as_view(), name='add_note'),
    path('notes/<int:pk>/edit/', NoteUpdateView.as_view(), name='edit_note'),
    path('notes/<int:pk>/delete/', NoteDeleteView.as_view(), name='delete_note'),
    
    # Reminder management
    path('reminders/', ReminderListView.as_view(), name='reminders'),
    path('reminders/add/', ReminderCreateView.as_view(), name='add_reminder'),
    path('reminders/<int:pk>/edit/', ReminderUpdateView.as_view(), name='edit_reminder'),
    path('reminders/<int:pk>/delete/', ReminderDeleteView.as_view(), name='delete_reminder'),
    path('reminders/<int:pk>/complete/', ToggleReminderCompleteView.as_view(), name='toggle_reminder_complete'),
    
    # Shortcut management
    path('shortcuts/', ShortcutListView.as_view(), name='shortcuts'),
    path('shortcuts/add/', ShortcutCreateView.as_view(), name='add_shortcut'),
    path('shortcuts/<int:pk>/edit/', ShortcutUpdateView.as_view(), name='edit_shortcut'),
    path('shortcuts/<int:pk>/delete/', ShortcutDeleteView.as_view(), name='delete_shortcut'),
    path('shortcuts/<int:pk>/toggle/', ToggleShortcutActiveView.as_view(), name='toggle_shortcut_active'),
]