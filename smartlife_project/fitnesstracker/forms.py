from django import forms
from .models import WorkoutPlan, Exercise, BodyStat, ActivityLog, FitnessGoal

class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ['goal_type', 'description', 'target_date', 'is_achieved', 'progress_percentage']

class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = '__all__'

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description', 'duration_weeks', 'difficulty_level', 'goal']

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'muscle_group', 'equipment', 'duration_minutes']

class BodyStatForm(forms.ModelForm):
    class Meta:
        model = BodyStat
        fields = ['weight_kg', 'height_cm', 'body_fat_percentage', 'muscle_mass_percentage', 'date']
