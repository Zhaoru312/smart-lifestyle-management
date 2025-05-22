from django.urls import path, include
from . import views
from .views import diettype_list, diettype_create, diettype_update, diettype_delete
from .views import supplement_list, supplement_create,supplement_update, supplement_delete

app_name = 'mealtracker'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('meals/', views.meal_list, name='meal_list'),
    path('meals/create/', views.meal_create, name='meal_create'),
    path('meals/<int:pk>/edit/', views.meal_update, name='meal_update'),
    path('meals/<int:pk>/delete/', views.meal_delete, name='meal_delete'),

    path('drinks/', views.drink_list, name='drink_list'),
    path('drinks/create/', views.drink_create, name='drink_create'),
    path('drinks/<int:pk>/edit/', views.drink_update, name='drink_update'),
    path('drinks/<int:pk>/delete/', views.drink_delete, name='drink_delete'),

    path('diettypes/', diettype_list, name='diettype_list'),
    path('diettypes/create/', diettype_create, name='diettype_create'),
    path('diettypes/<int:pk>/edit/', diettype_update, name='diettype_update'),
    path('diettypes/<int:pk>/delete/', diettype_delete, name='diettype_delete'),

    path('avoiditems/', views.avoiditem_list, name='avoiditem_list'),
    path('avoiditems/create/', views.avoiditem_create, name='avoiditem_create'),
    path('avoiditems/<int:pk>/edit/', views.avoiditem_update, name='avoiditem_update'),
    path('avoiditems/<int:pk>/delete/', views.avoiditem_delete, name='avoiditem_delete'),
    
    path('supplements/', supplement_list, name='supplement_list'),
    path('supplements/create/', supplement_create, name='supplement_create'),
    path('supplements/<int:pk>/edit/', supplement_update, name='supplement_update'),
    path('supplements/<int:pk>/delete/', supplement_delete, name='supplement_delete'),
]