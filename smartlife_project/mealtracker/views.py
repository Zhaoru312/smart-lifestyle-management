from django.shortcuts import render, redirect, get_object_or_404
from .models import Meal, Category
from .forms import MealForm

def meal_list(request):
    category_name = request.GET.get('category')
    if category_name:
        meals = Meal.objects.filter(category__name=category_name)
    else:
        meals = Meal.objects.all()

    categories = Category.objects.all()
    return render(request, 'mealtracker/meal_list.html', {
        'meals': meals,
        'categories': categories,
    })

def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    else:
        form = MealForm()
    return render(request, 'mealtracker/meal_form.html', {'form': form})

def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('meal_list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'mealtracker/meal_form.html', {'form': form})

def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        meal.delete()
        return redirect('meal_list')
    return render(request, 'mealtracker/meal_confirm_delete.html', {'meal': meal})
