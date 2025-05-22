from django.db import models

class BodyStat(models.Model):
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    body_fat_percentage = models.FloatField()
    muscle_mass_percentage = models.FloatField()
    date = models.DateField()

class WorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_weeks = models.IntegerField()
    difficulty_level = models.CharField(max_length=50)
    goal = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    muscle_group = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()

    def __str__(self):
        return self.name

class ActivityLog(models.Model):
    date = models.DateField()
    activity_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)  # untuk tambahan catatan

    def __str__(self):
        return f"{self.activity_type} on {self.date}"

class FitnessGoal(models.Model):
    GOAL_TYPES = [
        ('Lose Weight', 'Lose Weight'),
        ('Build Muscle', 'Build Muscle'),
        ('Increase Stamina', 'Increase Stamina'),
        ('Improve Flexibility', 'Improve Flexibility'),
        ('Other', 'Other'),
    ]

    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES)
    description = models.TextField()
    target_date = models.DateField()
    is_achieved = models.BooleanField(default=False)
    progress_percentage = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.goal_type} - {self.description[:20]}"
