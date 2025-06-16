from django.urls import path
from . import views

app_name = 'fitnesstracker'
urlpatterns = [
    path('', views.fitness_index, name='fitness_index'),
    path('workouts/', views.workout_plan_list, name='workout_plan_list'),
    path('workouts/add/', views.workout_plan_create, name='workout_plan_add'),
    path('workouts/edit/<int:pk>/', views.workout_plan_edit, name='workout_plan_edit'),
    path('workouts/delete/<int:pk>/', views.workout_plan_delete, name='workout_plan_delete'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercises/add/', views.exercise_add, name='exercise_add'),
    path('exercises/edit/<int:pk>/', views.exercise_edit, name='exercise_edit'),
    path('exercises/delete/<int:pk>/', views.exercise_delete, name='exercise_delete'),
    path('bodystats/', views.body_stat_list, name='body_stat_list'),
    path('bodystats/add/', views.body_stat_add, name='body_stat_add'),
    path('bodystats/edit/<int:pk>/', views.body_stat_edit, name='body_stat_edit'),
    path('bodystats/delete/<int:pk>/', views.body_stat_delete, name='body_stat_delete'),
    path('activity_logs/', views.activity_log_list, name='activity_log_list'),
    path('activity_logs/add/', views.activity_log_add, name='activity_log_add'),
    path('activity_logs/edit/<int:pk>/', views.activity_log_edit, name='activity_log_edit'),
    path('activity_logs/delete/<int:pk>/', views.activity_log_delete, name='activity_log_delete'),
    path('fitness_goals/', views.fitness_goal_list, name='fitness_goal_list'),
    path('fitness_goals/add/', views.fitness_goal_add, name='fitness_goal_add'),
    path('fitness_goals/edit/<int:pk>/', views.fitness_goal_edit, name='fitness_goal_edit'),
    path('fitness_goals/delete/<int:pk>/', views.fitness_goal_delete, name='fitness_goal_delete'),
]
