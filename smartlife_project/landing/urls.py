from django.urls import path
from .views import (
    IndexView, AuthView, LoginView, RegisterView, LogoutView,
    ContactView, FAQView, ForgotPasswordView, NewsletterSubscribeView
)

app_name = 'landing'
urlpatterns = [
    # Direct class-based view mappings
    path('', IndexView.as_view(), name='index'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('newsletter-subscribe/', NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),    
]
