from django.contrib import admin
from .models import WorkoutPlan, Exercise, BodyStat, ActivityLog, FitnessGoal

admin.site.register(WorkoutPlan)
admin.site.register(Exercise)
admin.site.register(BodyStat)
admin.site.register(ActivityLog)
admin.site.register(FitnessGoal)
