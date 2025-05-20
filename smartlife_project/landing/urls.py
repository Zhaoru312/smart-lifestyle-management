from django.urls import path
from . import views

app_name = 'landing'
urlpatterns = [
    # Direct class-based view mappings
    path('', views.IndexView.as_view(), name='index'),
    path('auth/', views.AuthView.as_view(), name='auth'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('newsletter-subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),    
]
