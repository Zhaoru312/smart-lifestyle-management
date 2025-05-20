from django.urls import path
from . import views

urlpatterns = [
    path('meal/', views.meal_list, name='meal_list'),
    path('meal/create/', views.meal_create, name='meal_create'),
    path('meal/<int:pk>/edit/', views.meal_update, name='meal_update'),
    path('meal/<int:pk>/delete/', views.meal_delete, name='meal_delete'),
]
