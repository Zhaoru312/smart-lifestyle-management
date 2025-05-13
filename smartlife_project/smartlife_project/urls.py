"""
URL configuration for smartlife_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.defaults import page_not_found, server_error

urlpatterns = [
    # Main app URLs
    path('', include('landing.urls')),
    path('dashboard/', include('dashboardmanager.urls')),
    path('finance/', include('financialmanagement.urls')),
    path('fitness/', include('fitnesstracker.urls')),
    path('habit/', include('habittracker.urls')),
    path('meal/', include('mealtracker.urls')),
    path('mental/', include('mentalhealth.urls')),
    path('tasks/', include('taskmanager.urls')),
    
    # Django admin
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# Error handlers - these are only used in production
handler404 = 'landing.views.custom_404_view'
handler500 = 'landing.views.custom_500_view'
handler403 = 'landing.views.custom_403_view'