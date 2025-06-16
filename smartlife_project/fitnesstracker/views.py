from django.shortcuts import render, redirect
from .models import WorkoutPlan, Exercise, BodyStat, ActivityLog, FitnessGoal
from .forms import WorkoutPlanForm, ExerciseForm, BodyStatForm, ActivityLogForm, FitnessGoalForm
from django.shortcuts import get_object_or_404

def fitness_goal_list(request):
    goals = FitnessGoal.objects.all()
    return render(request, 'fitnesstracker/fitness_goal_list.html', {'goals': goals})

def fitness_goal_add(request):
    if request.method == 'POST':
        form = FitnessGoalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:fitness_goal_list')
    else:
        form = FitnessGoalForm()
    return render(request, 'fitnesstracker/fitness_goal_form.html', {'form': form})

def fitness_goal_edit(request, pk):
    goal = get_object_or_404(FitnessGoal, pk=pk)
    if request.method == 'POST':
        form = FitnessGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:fitness_goal_list')
    else:
        form = FitnessGoalForm(instance=goal)
    return render(request, 'fitnesstracker/fitness_goal_form.html', {'form': form})

def fitness_goal_delete(request, pk):
    goal = get_object_or_404(FitnessGoal, pk=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('fitnesstracker:fitness_goal_list')
    return render(request, 'fitnesstracker/fitness_goal_confirm_delete.html', {'goal': goal})

def activity_log_list(request):
    logs = ActivityLog.objects.all().order_by('-date')
    return render(request, 'fitnesstracker/activity_log_list.html', {'logs': logs})

def activity_log_add(request):
    if request.method == 'POST':
        form = ActivityLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:activity_log_list')
    else:
        form = ActivityLogForm()
    return render(request, 'fitnesstracker/activity_log_form.html', {'form': form})

def activity_log_edit(request, pk):
    log = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        form = ActivityLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:activity_log_list')
    else:
        form = ActivityLogForm(instance=log)
    return render(request, 'fitnesstracker/activity_log_form.html', {'form': form})

def activity_log_delete(request, pk):
    log = get_object_or_404(ActivityLog, pk=pk)
    if request.method == 'POST':
        log.delete()
        return redirect('fitnesstracker:activity_log_list')
    return render(request, 'fitnesstracker/activity_log_confirm_delete.html', {'log': log})

def fitness_index(request):
    return render(request, 'fitnesstracker/index.html')

def workout_plan_create(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:workout_plan_list')
    else:
        form = WorkoutPlanForm()
    return render(request, 'fitnesstracker/workout_plan_form.html', {'form': form})

def workout_plan_edit(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:workout_plan_list')
    else:
        form = WorkoutPlanForm(instance=plan)
    return render(request, 'fitnesstracker/workout_plan_form.html', {'form': form})

def workout_plan_delete(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('fitnesstracker:workout_plan_list')
    return render(request, 'fitnesstracker/workout_plan_confirm_delete.html', {'plan': plan})

def body_stat_list(request):
    stats = BodyStat.objects.all().order_by('-date')
    if request.method == 'POST':
        form = BodyStatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:body_stat_list')
    else:
        form = BodyStatForm()
    
    return render(request, 'fitnesstracker/bodystats.html', {'stats': stats, 'form': form})

def workout_plan_list(request):
    plans = WorkoutPlan.objects.all()
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:workout_plan_list')
    else:
        form = WorkoutPlanForm()
    
    return render(request, 'fitnesstracker/workout_plan_list.html', {'plans': plans, 'form': form})

def exercise_list(request):
    exercises = Exercise.objects.all()
    return render(request, 'fitnesstracker/exercise_list.html', {'exercises': exercises})
    
def exercise_add(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'fitnesstracker/exercise_form.html', {'form': form})

def exercise_edit(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:exercise_list')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'fitnesstracker/exercise_form.html', {'form': form})

def exercise_delete(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('fitnesstracker:exercise_list')
    return render(request, 'fitnesstracker/exercise_confirm_delete.html', {'exercise': exercise})

def body_stat_list(request):
    stats = BodyStat.objects.all().order_by('-date')
    return render(request, 'fitnesstracker/bodystat_list.html', {'stats': stats})

def body_stat_add(request):
    if request.method == 'POST':
        form = BodyStatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:body_stat_list')
    else:
        form = BodyStatForm()
    return render(request, 'fitnesstracker/bodystat_form.html', {'form': form})

def body_stat_edit(request, pk):
    stat = get_object_or_404(BodyStat, pk=pk)
    if request.method == 'POST':
        form = BodyStatForm(request.POST, instance=stat)
        if form.is_valid():
            form.save()
            return redirect('fitnesstracker:body_stat_list')
    else:
        form = BodyStatForm(instance=stat)
    return render(request, 'fitnesstracker/bodystat_form.html', {'form': form})

def body_stat_delete(request, pk):
    stat = get_object_or_404(BodyStat, pk=pk)
    if request.method == 'POST':
        stat.delete()
        return redirect('fitnesstracker:body_stat_list')
    return render(request, 'fitnesstracker/bodystat_confirm_delete.html', {'stat': stat})
