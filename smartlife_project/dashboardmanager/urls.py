from django.urls import path
from . import views

app_name = 'dashboardmanager'

urlpatterns = [
    path('', views.index, name='index'),
    path('applist/', views.applist, name='applist'),
    path('profile/', views.profile, name='profile'),
    path('layouts/', views.list_layouts, name='list_layouts'),
    path('layouts/create/', views.create_layout, name='create_layout'),
    path('layouts/<int:pk>/', views.view_layout, name='view_layout'),
    path('layouts/<int:pk>/edit/', views.edit_layout, name='edit_layout'),
    path('layouts/<int:pk>/delete/', views.delete_layout, name='delete_layout'),
    path('layouts/<int:pk>/set_default/', views.set_default_layout, name='set_default_layout'),
    path('landing/', views.landing_page, name='landing_page'),
    path('landing/hero/<int:pk>/', views.update_hero_section, name='update_hero_section'),
    path('landing/feature/<int:pk>/', views.update_feature, name='update_feature'),
    path('landing/testimonial/<int:pk>/', views.update_testimonial, name='update_testimonial'),
    path('landing/faq/<int:pk>/', views.update_faq, name='update_faq'),
]