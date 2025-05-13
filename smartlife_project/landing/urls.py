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
    
    # Keep function-based views for backward compatibility
    # These will be removed once we confirm everything works correctly
    # path('', views.index, name='index_old'),
    # path('auth/', views.auth_view, name='auth_old'),
    # path('login/', views.login_view, name='login_old'),
    # path('register/', views.register_view, name='register_old'),
    # path('logout/', views.logout_view, name='logout_old'),
    # path('contact/', views.contact_view, name='contact_old'),
    # path('faq/', views.faq_view, name='faq_old'),
    # path('forgot-password/', views.forgot_password_view, name='forgot_password_old'),
    # path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe_old'),
]