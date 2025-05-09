from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user': request.user,
        'apps': [
            {'name': 'Finance', 'url': '/finance/', 'icon': 'fas fa-wallet'},
            {'name': 'Fitness', 'url': '/fitness/', 'icon': 'fas fa-dumbbell'},
            {'name': 'Habit', 'url': '/habit/', 'icon': 'fas fa-repeat'},
            {'name': 'Meal', 'url': '/meal/', 'icon': 'fas fa-utensils'},
            {'name': 'Mental', 'url': '/mental/', 'icon': 'fas fa-brain'},
            {'name': 'Tasks', 'url': '/tasks/', 'icon': 'fas fa-tasks'}
        ]
    }
    
    return render(request, 'dashboardmanager/index.html', context)