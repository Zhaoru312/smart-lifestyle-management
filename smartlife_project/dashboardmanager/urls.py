from django.urls import path
from . import views

app_name = 'dashboardmanager'

urlpatterns = [
    path('', views.index, name='index'),
]