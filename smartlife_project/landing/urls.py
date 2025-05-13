from django.urls import path
from . import views

app_name = 'landing'
urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),  # New unified authentication view
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]