from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Project(models.Model):
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
    
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        blank=True, 
        null=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    color = models.CharField(
        max_length=7, 
        default='#3498db'
    )
    start_date = models.DateField()
    due_date = models.DateField()
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'name']
        ordering = ['-is_active', 'name']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.due_date and self.start_date and self.due_date < self.start_date:
            raise ValidationError('Due date cannot be before start date')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(
        max_length=50
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='categories'
    )
    color = models.CharField(
        max_length=7, 
        default="#3498db"
    )
    is_default = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = ['user', 'name']
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        # Ensure only one default category per user
        if self.is_default:
            query = Category.objects.filter(user=self.user, is_default=True)
            if self.pk:  # If editing, exclude current category
                query = query.exclude(pk=self.pk)
            if query.exists():
                raise ValidationError('You can only have one default category')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    title = models.CharField(
        max_length=200
    )
    description = models.TextField(
        blank=True, 
        null=True
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tasks'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tasks'
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    scheduled_time = models.TimeField(
        null=True, 
        blank=True
    )
    deadline = models.DateField()
    is_completed = models.BooleanField(
        default=False
    )
    progress = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return self.title
    
    def calculate_progress(self):
        """Calculate task progress based on subtasks"""
        subtasks = self.subtasks.all()
        if not subtasks:
            return 100 if self.is_completed else 0
            
        total = subtasks.count()
        completed = subtasks.filter(is_completed=True).count()
        
        if total == 0:
            return 0
        
        return int((completed / total) * 100)
    
    def update_progress(self):
        """Update progress field based on subtasks completion"""
        self.progress = self.calculate_progress()
        self.save(update_fields=['progress'])
        
    def is_overdue(self):
        """Check if task is overdue"""
        if not self.deadline:
            return False
        return self.deadline < timezone.now().date() and not self.is_completed

class Subtask(models.Model):
    task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='subtasks'
    )
    title = models.CharField(
        max_length=200
    )
    is_completed = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        verbose_name_plural = 'Subtasks'
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if len(self.title.strip()) < 3:
            raise ValidationError('Title must be at least 3 characters long')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # Update parent task progress when subtask is saved
        if hasattr(self, 'task'):
            self.task.update_progress()

class TaskActivity(models.Model):
    ACTIVITY_TYPES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('complete', 'Completed'),
        ('delete', 'Deleted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='activities', null=True)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Task Activities"
        
    def __str__(self):
        return f"{self.user.username} {self.activity_type} task: {self.task.title if self.task else 'Deleted task'}"