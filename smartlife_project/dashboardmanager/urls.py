from django.urls import path
from . import views

app_name = 'dashboardmanager'

urlpatterns = [
    # Dashboard main views
    path('', views.index, name='index'),
    path('applist/', views.applist, name='applist'),
    path('profile/', views.profile, name='profile'),
    
    # Landing page management
    path('landing/', views.landing_page, name='landing_page'),
    path('landing/hero/<int:pk>/', views.update_hero_section, name='update_hero_section'),
    path('landing/feature/<int:pk>/', views.update_feature, name='update_feature'),
    path('landing/testimonial/<int:pk>/', views.update_testimonial, name='update_testimonial'),
    path('landing/faq/<int:pk>/', views.update_faq, name='update_faq'),
    path('landing/hero/<int:pk>/delete/', views.delete_hero_section, name='delete_hero_section'),
    path('landing/feature/<int:pk>/delete/', views.delete_feature, name='delete_feature'),
    path('landing/testimonial/<int:pk>/delete/', views.delete_testimonial, name='delete_testimonial'),
    path('landing/faq/<int:pk>/delete/', views.delete_faq, name='delete_faq'),
    
    # Bookmark management
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('bookmarks/add/', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/<int:pk>/edit/', views.edit_bookmark, name='edit_bookmark'),
    path('bookmarks/<int:pk>/delete/', views.delete_bookmark, name='delete_bookmark'),
    
    # Note management
    path('notes/', views.note_list, name='note_list'),
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('notes/<int:pk>/delete/', views.delete_note, name='delete_note'),
    
    # Reminder management
    path('reminders/', views.reminder_list, name='reminder_list'),
    path('reminders/add/', views.add_reminder, name='add_reminder'),
    path('reminders/<int:pk>/edit/', views.edit_reminder, name='edit_reminder'),
    path('reminders/<int:pk>/delete/', views.delete_reminder, name='delete_reminder'),
    path('reminders/<int:pk>/complete/', views.toggle_reminder_complete, name='toggle_reminder_complete'),
    
    # Shortcut management
    path('shortcuts/', views.shortcut_list, name='shortcut_list'),
    path('shortcuts/add/', views.add_shortcut, name='add_shortcut'),
    path('shortcuts/<int:pk>/edit/', views.edit_shortcut, name='edit_shortcut'),
    path('shortcuts/<int:pk>/delete/', views.delete_shortcut, name='delete_shortcut'),
    path('shortcuts/<int:pk>/toggle/', views.toggle_shortcut_active, name='toggle_shortcut_active'),
]