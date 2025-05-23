from django import forms
from django.utils import timezone
from .models import Project, Category, Task, Subtask

class ColorSelect(forms.RadioSelect):
    option_template_name = 'taskmanager/widgets/color_radio_option.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs = {'class': 'color-radio-select'}

class ProjectForm(forms.ModelForm):
    # Define color choices as a class variable for easy reuse
    COLOR_CHOICES = [
        ('#3498db', 'Blue'),
        ('#2ecc71', 'Green'),
        ('#e74c3c', 'Red'),
        ('#f39c12', 'Orange'),
        ('#9b59b6', 'Purple'),
        ('#1abc9c', 'Turquoise'),
        ('#e67e22', 'Carrot'),
        ('#e84393', 'Pink'),
    ]
    
    # Override color field to use our choices
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=ColorSelect,
        initial='#3498db',
        help_text='Select a color to identify this project',
        required=True,
        label='Project Color'
    )
    
    # Define date fields with proper widget configuration
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'YYYY-MM-DD',
            'min': timezone.now().strftime('%Y-%m-%d'),
            'required': True
        }),
        required=True,
        label='Start Date *',
        help_text='The date when the project will start (required)'
    )
    
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
            'min': timezone.now().strftime('%Y-%m-%d'),
            'required': 'required'
        }),
        required=True,
        label='Due Date *',
        help_text='The target completion date for the project (required)'
    )
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'due_date', 'color', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name',
                'minlength': '3',
                'maxlength': '100',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Enter project description (optional)',
                'maxlength': '500',
                'required': False
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'required': True
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD',
                'required': True
            }),
            'is_active': forms.HiddenInput()
        }
        labels = {
            'name': 'Project Name',
            'description': 'Description',
            'is_active': 'Active',
            'start_date': 'Project start date',
            'due_date': 'Project due date',
        }
        help_texts = {
            'name': 'A clear, descriptive name (3-100 characters)',
            'description': 'Provide context and details about this project (max 500 characters)',
            'color': 'Choose a color to visually identify this project',
        }
    
    def __init__(self, *args, **kwargs):
        # Extract user from kwargs before calling parent's __init__
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set the minimum date/time for the due date based on start date
        if 'start_date' in self.initial:
            min_due_date = self.initial['start_date']
            if min_due_date:
                self.fields['due_date'].widget.attrs['min'] = min_due_date.strftime('%Y-%m-%dT%H:%M')
        
        # Set initial active status to True for new projects
        if not self.instance.pk:
            self.fields['is_active'].initial = True
            
        # Add common attributes to fields
        for field_name, field in self.fields.items():
            if field_name != 'is_active':  # Skip hidden fields
                # Add data-controller for date fields
                if field_name in ['start_date', 'due_date']:
                    field.widget.attrs['data-controller'] = 'datepicker'
                
                # Add placeholder if not set
                if not field.widget.attrs.get('placeholder') and field_name != 'color' and hasattr(field, 'label'):
                    field.widget.attrs['placeholder'] = f'Enter {field.label.lower()}'
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError('Start date cannot be in the past')
            
        if start_date and due_date and due_date < start_date:
            raise forms.ValidationError('Due date must be after the start date')
            
        return cleaned_data
    
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Project name is required')
        
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
        
        if len(name) > 100:
            raise forms.ValidationError('Project name cannot exceed 100 characters')
        
        # Check for duplicate project names for this user (case-insensitive)
        if self.user:
            query = Project.objects.filter(
                user=self.user, 
                name__iexact=name
            )
            if self.instance.pk:  # If editing, exclude current project
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError('You already have a project with this name.')
        
        return name
    
    def save(self, commit=True):
        project = super().save(commit=False)
        if self.user:
            project.user = self.user
        if commit:
            project.save()
        return project

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Work, Personal, Shopping',
                'minlength': '3',
                'maxlength': '50'
            }),
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'title': 'Choose a color for this category'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'data-bs-toggle': 'tooltip',
                'title': 'Set as default category for new tasks'
            })
        }
        help_texts = {
            'name': 'A short, unique name (3-50 characters)',
            'color': 'Choose a color to visually identify this category',
            'is_default': 'Make this the default category for new tasks (only one allowed)'
        }
        labels = {
            'name': 'Category Name',
            'is_default': 'Set as default category'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add data-controller for color picker
        if 'color' in self.fields:
            self.fields['color'].widget.attrs['data-controller'] = 'color-picker'
    
    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('Category name is required')
            
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters long')
            
        # Check for duplicate names (case-insensitive) for this user
        if self.user:
            query = Category.objects.filter(
                user=self.user, 
                name__iexact=name
            )
            if self.instance.pk:  # If editing, exclude current category
                query = query.exclude(pk=self.instance.pk)
                
            if query.exists():
                raise forms.ValidationError('You already have a category with this name')
                
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        is_default = cleaned_data.get('is_default')
        
        # If setting as default, ensure no other default exists for this user
        if is_default and self.user:
            query = Category.objects.filter(
                user=self.user, 
                is_default=True
            )
            if self.instance.pk:  # If editing, exclude current category
                query = query.exclude(pk=self.instance.pk)
                
            if query.exists():
                self.add_error(
                    'is_default',
                    'You already have a default category. Uncheck the other one first.'
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        category = super().save(commit=False)
        if not category.pk:  # New category
            category.user = self.user
        
        if commit:
            category.save()
            
            # If this is set as default, ensure no other categories are default
            if category.is_default:
                Category.objects.filter(
                    user=category.user, 
                    is_default=True
                ).exclude(pk=category.pk).update(is_default=False)
                
        return category

class TaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Filter projects and categories by user
        self.fields['project'].queryset = Project.objects.filter(
            user=user, 
            is_active=True
        ).order_by('name')
        
        self.fields['category'].queryset = Category.objects.filter(
            user=user
        ).order_by('name')
        
        # Set default category if available and not set
        if not self.instance.pk and 'category' not in self.data:
            default_category = Category.objects.filter(
                user=user, 
                is_default=True
            ).first()
            if default_category:
                self.fields['category'].initial = default_category
        
        # Add data-controller for datepicker on deadline field
        if 'deadline' in self.fields:
            self.fields['deadline'].widget.attrs.update({
                'data-controller': 'datepicker',
                'min': timezone.now().strftime('%Y-%m-%d')
            })
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'category', 'priority', 
                 'scheduled_time', 'deadline', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Complete project report, Buy groceries',
                'minlength': '3',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add details, notes, or requirements for this task...',
                'maxlength': '1000',
                'data-controller': 'character-counter',
                'data-character-counter-limit': '1000'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select',
                'data-controller': 'select2',
                'data-placeholder': 'Select a project (optional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'data-controller': 'select2',
                'data-placeholder': 'Select a category (optional)'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'data-controller': 'select2'
            }),
            'scheduled_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': '--:-- --'
            }),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
                'min': timezone.now().strftime('%Y-%m-%d'),
                'required': 'required'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'data-action': 'change->task#toggleComplete',
                'data-bs-toggle': 'tooltip',
                'title': 'Mark as completed'
            })
        }
        help_texts = {
            'title': 'A clear, descriptive name (3-200 characters)',
            'description': 'Additional details, notes, or requirements (max 1000 characters)',
            'project': 'Optional: Group this task under a project',
            'category': 'Optional: Categorize this task',
            'priority': 'Set the priority level for better organization',
            'scheduled_time': 'Optional: Specific time to work on this task',
            'deadline': 'Optional: Due date for this task',
            'is_completed': 'Mark when the task is finished'
        }
        labels = {
            'title': 'Task Title',
            'description': 'Task Details',
            'scheduled_time': 'Scheduled Time',
            'is_completed': 'Mark as Complete'
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Task title is required')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long')
        return title
    
    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if not deadline:
            raise forms.ValidationError("Deadline is required.")
        if deadline < timezone.now().date():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return deadline
    
    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        category = cleaned_data.get('category')
        
        # Ensure task has either project or category or both
        if not project and not category:
            raise forms.ValidationError('A task must have either a project or a category (or both)')
        
        # Ensure project belongs to user if provided
        if project and project.user != self.user:
            raise forms.ValidationError('Invalid project selected')
        
        # Ensure category belongs to user if provided
        if category and category.user != self.user:
            raise forms.ValidationError('Invalid category selected')
        
        return cleaned_data
    
    def save(self, commit=True):
        task = super().save(commit=False)
        
        # Set user for new tasks
        if not task.pk:
            task.user = self.user
        
        # Update progress if completion status changed
        if 'is_completed' in self.changed_data:
            task.progress = 100 if task.is_completed else 0
        
        if commit:
            task.save()
            
        return task

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['title', 'task', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subtask title',
                'required': 'required'
            }),
            'task': forms.HiddenInput(),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        help_texts = {
            'title': 'A clear description of this step (3-200 characters)',
            'is_completed': 'Mark as completed'
        }
        labels = {
            'title': 'Subtask',
            'is_completed': 'Completed'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Ensure title field has form-control class
        self.fields['title'].widget.attrs['class'] = 'form-control'
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Subtask title is required')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long')
        return title
        
    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get('task')
        
        if not task:
            raise forms.ValidationError('A task must be specified for this subtask')
            
        return cleaned_data
        
    def save(self, commit=True):
        subtask = super().save(commit=False)
        if commit:
            subtask.save()
            self.save_m2m()
        return subtask