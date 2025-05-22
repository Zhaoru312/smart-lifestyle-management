from django.urls import path
from . import views

app_name = 'taskmanager'
urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Step-by-step creation
    path('create/', views.create_project, name='create_workflow'),
    path('create/task/<int:project_id>/', views.create_task, name='create_task_workflow'),
    path('create/subtask/<int:task_id>/', views.create_subtask, name='create_subtask_workflow'),
    
    # Project management
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Task management
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/toggle-complete/', views.task_toggle_complete, name='task_toggle_complete'),
    
    # Category management
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/create/', views.categories_create, name='categories_create'),
    
    # Subtask management
    path('subtasks/<int:pk>/', views.subtask_detail, name='subtask_detail'),
    path('subtasks/<int:pk>/update/', views.subtask_update, name='subtask_update'),
    path('subtasks/<int:pk>/delete/', views.subtask_delete, name='subtask_delete'),
    path('subtasks/<int:pk>/toggle-complete/', views.subtask_toggle_complete, name='subtask_toggle_complete'),
]