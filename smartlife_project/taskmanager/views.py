from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Project, Category, Task, Subtask, TaskActivity
from .forms import ProjectForm, CategoryForm, TaskForm, SubtaskForm

# ===== PROJECT VIEWS =====
@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'taskmanager/index.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related(
        'tasks__subtasks'
    ), pk=pk, user=request.user)
    
    # Get active and completed tasks
    active_tasks = project.tasks.filter(is_completed=False).annotate(
        completed_subtasks_count=Count('subtasks', filter=Q(subtasks__is_completed=True))
    ).order_by('-created_at')
    
    completed_tasks = project.tasks.filter(is_completed=True).order_by('-updated_at')
    
    # Calculate project progress
    total_tasks = project.tasks.count()
    completed_tasks_count = completed_tasks.count()
    project.progress = int((completed_tasks_count / total_tasks) * 100) if total_tasks > 0 else 0
    
    return render(request, 'taskmanager/projects/detail.html', {
        'project': project,
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
    })

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, user=request.user)
        if form.is_valid():
            project = form.save(commit=False)
            project.updated_at = timezone.now()
            project.save()
            
            # Log activity
            TaskActivity.objects.create(
                task=None,
                user=request.user,
                activity_type='updated',
                description=f'Updated project "{project.name}"'
            )
            
            messages.success(request, 'Project updated successfully!')
            return redirect('taskmanager:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project, user=request.user)
    
    return render(request, 'taskmanager/projects/update.html', {
        'form': form,
        'project': project,
        'title': 'Edit Project'
    })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('taskmanager:project_list')
    return render(request, 'projects/delete.html', {'project': project})

# ===== TASK VIEWS =====
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    
    # Filtering
    project_id = request.GET.get('project')
    category_id = request.GET.get('category')
    completed = request.GET.get('completed')
    
    if project_id:
        tasks = tasks.filter(project_id=project_id)
    if category_id:
        tasks = tasks.filter(category_id=category_id)
    if completed == 'true':
        tasks = tasks.filter(is_completed=True)
    elif completed == 'false':
        tasks = tasks.filter(is_completed=False)
    
    return render(request, 'taskmanager/tasks/list.html', {
        'tasks': tasks,
        'projects': Project.objects.filter(user=request.user),
        'categories': Category.objects.filter(user=request.user)
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('taskmanager:task_list')
    else:
        form = TaskForm(request.user)
    return render(request, 'tasks/create.html', {'form': form})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(
        Task.objects.select_related('project')
                   .prefetch_related('subtasks', 'activities')
                   .annotate(
                       completed_subtasks_count=Count('subtasks', filter=Q(subtasks__is_completed=True))
                   ),
        pk=pk,
        user=request.user
    )
    
    # Log view activity if not already logged
    if not task.activities.filter(activity_type='viewed').exists():
        TaskActivity.objects.create(
            task=task,
            user=request.user,
            activity_type='viewed',
            description=f'Viewed the task "{task.title}"'
        )
    
    return render(request, 'taskmanager/projects/task_detail.html', {
        'task': task,
        'activities': task.activities.all().order_by('-created_at')[:10],
        'has_project': hasattr(task, 'project') and task.project is not None
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.updated_at = timezone.now()
            task.save()
            
            # Log activity
            TaskActivity.objects.create(
                task=task,
                user=request.user,
                activity_type='updated',
                description=f'Updated the task "{task.title}"'
            )
            
            messages.success(request, 'Task updated successfully!')
            
            return redirect('taskmanager:task_detail', pk=task.pk)
    else:
        form = TaskForm(request.user, instance=task)
    
    return render(request, 'taskmanager/projects/task_update.html', {
        'form': form,
        'task': task,
        'title': 'Edit Task'
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('taskmanager:project_detail', pk=task.project.pk)
    return render(request, 'tasks/delete.html', {'task': task})

@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.is_completed = not task.is_completed
        task.completed_at = timezone.now() if task.is_completed else None
        task.save()
        
        # Update all subtasks to match task completion status
        task.subtasks.update(
            is_completed=task.is_completed,
            updated_at=timezone.now()
        )
        
        # Log activity
        TaskActivity.objects.create(
            user=request.user,
            task=task,
            activity_type='completed' if task.is_completed else 'reopened',
            description=f"Task marked as {'completed' if task.is_completed else 'incomplete'}: {task.title}"
        )
        
        messages.success(
            request, 
            f'Task marked as {"completed" if task.is_completed else "incomplete"} successfully!'
        )
    
    return redirect('taskmanager:task_detail', pk=task.id)


# ===== CATEGORY VIEWS =====
@login_required
def categories_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'taskmanager/categories/list.html', {'categories': categories})

@login_required
def categories_create(request):
    if request.method == 'POST':
        # Create a mutable copy of the POST data
        post_data = request.POST.copy()
        
        # Create form with user and POST data
        form = CategoryForm(post_data, user=request.user)
        
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    # Return JSON response for AJAX requests
                    return JsonResponse({
                        'success': True,
                        'category_id': category.id,
                        'category_name': str(category)
                    })
                
                # Add success message for non-AJAX requests
                messages.success(request, 'Category created successfully!')
                next_url = request.POST.get('next', reverse('taskmanager:categories_list'))
                return redirect(next_url)
                
            except Exception as e:
                error_msg = str(e)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': error_msg
                    }, status=400)
                messages.error(request, f'Error creating category: {error_msg}')
        else:
            # Handle form errors
            error_msgs = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_msgs.append(f"{field}: {error}")
            
            error_msg = ", ".join(error_msgs)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': error_msg,
                    'errors': form.errors
                }, status=400)
            messages.error(request, error_msg)
    else:
        form = CategoryForm(user=request.user)
    
    # Only render the template for non-AJAX requests
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'taskmanager/categories/create.html', {
            'form': form,
            'next': request.GET.get('next', '')
        })
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# ===== SUBTASK VIEWS =====
@login_required
def subtask_detail(request, pk):
    subtask = get_object_or_404(
        Subtask.objects.select_related('task', 'task__project'),
        pk=pk,
        task__user=request.user
    )
    
    # Log view activity if not already logged
    if not hasattr(subtask, 'activities') or not subtask.activities.filter(activity_type='viewed').exists():
        TaskActivity.objects.create(
            task=subtask.task,
            user=request.user,
            activity_type='viewed',
            description=f'Viewed the subtask "{subtask.title}"'
        )
    
    return render(request, 'taskmanager/projects/subtask_detail.html', {
        'subtask': subtask
    })

@login_required
def subtask_update(request, pk):
    subtask = get_object_or_404(Subtask, pk=pk, task__user=request.user)
    
    if request.method == 'POST':
        # Fix: Pass data first, then use instance parameter for the subtask
        form = SubtaskForm(request.POST, instance=subtask, user=request.user)
        if form.is_valid():
            subtask = form.save()
            
            # Update parent task progress
            subtask.task.update_progress()
            
            # Log activity
            TaskActivity.objects.create(
                task=subtask.task,
                user=request.user,
                activity_type='updated',
                description=f'Updated subtask "{subtask.title}"',
            )
            
            messages.success(request, 'Subtask updated successfully!')
            return redirect('taskmanager:task_detail', pk=subtask.task.pk)
    else:
        # Fix: Use instance parameter and pass user as keyword argument
        form = SubtaskForm(instance=subtask, user=request.user)
    
    return render(request, 'taskmanager/projects/subtask_form.html', {
        'form': form,
        'subtask': subtask,
        'task': subtask.task,
        'title': 'Update Subtask',
        'form_action': 'update'
    })

@login_required
def subtask_create(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    
    if request.method == 'POST':
        form = SubtaskForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                # Create subtask and assign the task
                subtask = form.save(commit=False)
                subtask.task = task  # Assign the task from URL parameter
                subtask.save()
                
                # Update parent task progress
                task.update_progress()
                
                # Log activity
                TaskActivity.objects.create(
                    task=task,
                    user=request.user,
                    activity_type='created',
                    description=f'Created subtask "{subtask.title}"',
                )
                
                messages.success(request, 'Subtask created successfully!')
                return redirect('taskmanager:task_detail', pk=task.pk)
                
            except Exception as e:
                messages.error(request, f'Error creating subtask: {str(e)}')
    else:
        form = SubtaskForm(user=request.user)
    
    return render(request, 'taskmanager/projects/subtask_form.html', {
        'form': form,
        'task': task,  # Pass task to template for back button
        'title': 'Create New Subtask',
        'form_action': 'create'
    })
    
@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(
        Subtask.objects.select_related('task'),
        pk=pk,
        task__user=request.user
    )
    
    task_id = subtask.task.id
    subtask_title = subtask.title
    
    # Log activity before deletion
    TaskActivity.objects.create(
        task=subtask.task,
        user=request.user,
        activity_type='deleted',
        description=f'Deleted subtask "{subtask_title}"'
    )
    
    subtask.delete()
    
    messages.success(request, f'Subtask "{subtask_title}" has been deleted.')
    return redirect('taskmanager:task_detail', pk=task_id)

@login_required
def subtask_toggle_complete(request, pk):
    subtask = get_object_or_404(Subtask, pk=pk, task__user=request.user)
    if request.method == 'POST':
        subtask.is_completed = not subtask.is_completed
        subtask.save()
        subtask.task.update_progress()
    return redirect('taskmanager:task_detail', pk=subtask.task.id)

# ===== STEP-BY-STEP CREATION =====
@login_required
def create_project(request):
    """First step: Create a new project"""
    if request.method == 'POST':
        form = ProjectForm(data=request.POST, user=request.user)  # Pass user as keyword argument
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            # Add success message
            messages.success(request, 'Project created successfully! Now add tasks.')
            # Include namespace in redirect
            return redirect('taskmanager:create_task_workflow', project_id=project.id)
    else:
        form = ProjectForm(user=request.user)  # Pass user as keyword argument
    
    return render(request, 'taskmanager/create/project.html', {
        'form': form,
        'step': 1,
        'total_steps': 3,
        'current_title': 'Create Project',
        'color_choices': Project.COLOR_CHOICES  # Pass color choices to template
    })

@login_required
def create_task(request, project_id):
    """Second step: Create a task for the project"""
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.project = project
            task.save()
            
            # Log activity
            TaskActivity.objects.create(
                task=task,
                user=request.user,
                activity_type='created',
                description=f'Created task "{task.title}"'
            )
            
            if 'save_and_add_another' in request.POST:
                messages.success(request, 'Task created successfully! Add another task below.')
                return redirect('taskmanager:create_task_workflow', project_id=project.id)
            else:
                messages.success(request, 'Task created successfully! Now add subtasks.')
                return redirect('taskmanager:create_subtask_workflow', task_id=task.id)
    else:
        form = TaskForm(request.user)
    
    return render(request, 'taskmanager/create/task.html', {
        'form': form,
        'project': project,
        'step': 2,
        'total_steps': 3,
        'current_title': 'Add Task',
        'color_choices': Project.COLOR_CHOICES
    })

@login_required
def create_subtask(request, task_id):
    """Third step: Add subtasks to the task"""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        if 'finish' in request.POST:
            # Handle finish button click
            messages.success(request, 'Task created successfully!')
            last_subtask = task.subtasks.last()
            if last_subtask:
                return redirect('taskmanager:subtask_detail', pk=last_subtask.id)
            return redirect('taskmanager:task_detail', pk=task.id)
        
        # Create a mutable copy of the POST data
        post_data = request.POST.copy()
        # Ensure task is set in the form data
        post_data['task'] = task.id
        
        # Handle add subtask form submission
        form = SubtaskForm(post_data)
        if form.is_valid():
            try:
                subtask = form.save(commit=False)
                subtask.task = task  # Ensure task is set from URL
                subtask.save()
                task.update_progress()
                messages.success(request, 'Subtask added successfully!')
                return redirect('taskmanager:create_subtask_workflow', task_id=task.id)
            except Exception as e:
                messages.error(request, f'Error saving subtask: {str(e)}')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field}: {error}")
    else:
        # Initialize form with task pre-filled
        form = SubtaskForm(initial={'task': task.id})
    
    subtasks = task.subtasks.all()
    
    return render(request, 'taskmanager/create/subtask.html', {
        'form': form,
        'task': task,
        'subtasks': subtasks,
        'step': 3,
        'total_steps': 3,
        'current_title': 'Add Subtasks',
        'color_choices': Project.COLOR_CHOICES
    })

# ===== DASHBOARD VIEW =====
@login_required
def dashboard(request):
    # Get filter parameters with default values
    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category')
    priority = request.GET.get('priority')
    show_completed = request.GET.get('show_completed') == 'on'

    # Base queries
    all_tasks = Task.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user).order_by('-updated_at')
    
    # Apply project filters first (search)
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Check if any task filters are applied (excluding show_completed)
    has_task_filters = any([category_id, priority])
    
    # Always get all tasks for the projects
    tasks = all_tasks.filter(project__in=projects)
    
    # Apply task filters if any
    if category_id and category_id.isdigit():
        tasks = tasks.filter(category_id=category_id)
    
    if priority:
        tasks = tasks.filter(priority=priority)
    
    # Apply show_completed filter to tasks
    filtered_tasks = tasks.filter(is_completed=False) if not show_completed else tasks
    
    # Get the list of project IDs that have matching tasks
    project_ids_with_tasks = filtered_tasks.values_list('project_id', flat=True).distinct()
    
    # If no task filters are applied, include all projects
    if not has_task_filters:
        # Annotate all projects with their task counts
        projects = projects.annotate(
            task_count=Count(
                'tasks',
                filter=Q(tasks__in=filtered_tasks) if not show_completed else Q()
            ),
            completed_count=Count(
                'tasks',
                filter=Q(tasks__is_completed=True) if show_completed else Q(pk__isnull=True)
            )
        )
    else:
        # When task filters are applied, only show projects with matching tasks
        projects = projects.filter(id__in=project_ids_with_tasks).annotate(
            task_count=Count(
                'tasks',
                filter=Q(tasks__in=filtered_tasks)
            ),
            completed_count=Count(
                'tasks',
                filter=Q(tasks__in=filtered_tasks, tasks__is_completed=True)
            )
        )
    
    # Calculate statistics based on all tasks (unfiltered)
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(is_completed=True).count()
    in_progress_tasks = all_tasks.filter(is_completed=False).count()
    
    # Calculate completion percentage (avoid division by zero)
    completion_percentage = 0
    if total_tasks > 0:
        completion_percentage = round((completed_tasks / total_tasks) * 100)
    
    # Get statistics for the dashboard
    stats = {
        'total': total_tasks,
        'completed': completed_tasks,
        'active': in_progress_tasks,
        'overdue': all_tasks.filter(
            deadline__lt=timezone.now().date(),
            is_completed=False
        ).count(),
        'due_today': all_tasks.filter(
            deadline=timezone.now().date(),
            is_completed=False
        ).count(),
        'high_priority': all_tasks.filter(
            priority='high',
            is_completed=False
        ).count()
    }
    
    recent_tasks = tasks.order_by('-created_at')[:5]
    recent_activities = TaskActivity.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    # Get all categories for the filter dropdown
    categories = Category.objects.filter(user=request.user)
    priorities = [
        {'value': 'high', 'label': 'High'},
        {'value': 'medium', 'label': 'Medium'},
        {'value': 'low', 'label': 'Low'}
    ]
    
    context = {
        'projects': projects,
        'tasks': tasks,
        'stats': stats,
        'categories': categories,
        'priorities': priorities,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': in_progress_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage,
        'recent_activities': recent_activities,
        'recent_tasks': recent_tasks,
        'filter_values': {
            'search': search_query,
            'category': int(category_id) if category_id and category_id.isdigit() else '',
            'priority': priority,
            'show_completed': show_completed
        }
    }
    
    return render(request, 'taskmanager/index.html', context)