from django.urls import path
from . import views

app_name = 'dashboardmanager'

urlpatterns = [
    path('', views.index, name='index'),
    path('landing/', views.landing_page, name='landing_page'),
    path('landing/hero/<int:pk>/', views.update_hero_section, name='update_hero_section'),
    path('landing/feature/<int:pk>/', views.update_feature, name='update_feature'),
    path('landing/testimonial/<int:pk>/', views.update_testimonial, name='update_testimonial'),
    path('landing/faq/<int:pk>/', views.update_faq, name='update_faq'),
]