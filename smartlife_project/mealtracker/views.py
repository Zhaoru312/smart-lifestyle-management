from django.shortcuts import render, redirect, get_object_or_404
from .models import Meal, Category, Drink, DietType, AvoidItem, Supplement
from .forms import MealForm, DrinkForm, DietTypeForm, AvoidItemForm, SupplementForm
from django.contrib.auth.decorators import login_required

#dashboard
@login_required
def dashboard(request):
    meals = Meal.objects.all()
    drinks = Drink.objects.all()
    diettypes = DietType.objects.all()
    avoiditems = AvoidItem.objects.all()
    supplements = Supplement.objects.all()
    
    return render(request, 'index.html', {'meals': meals, 'drinks': drinks, 'diettypes': diettypes, 'avoiditems': avoiditems, 'supplements': supplements})

#meal
@login_required
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

@login_required
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:meal_list')
    else:
        form = MealForm()
    return render(request, 'mealtracker/meal_form.html', {'form': form})

@login_required
def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:meal_list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'mealtracker/meal_form.html', {'form': form})

@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        meal.delete()
        return redirect('mealtracker:meal_list')
    return render(request, 'mealtracker/meal_confirm_delete.html', {'meal': meal})

#drink
@login_required
def drink_list(request):
    drinks = Drink.objects.all()
    return render(request, 'mealtracker/drink_list.html', {'drinks': drinks})

@login_required
def drink_create(request):
    if request.method == 'POST':
        form = DrinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:drink_list')
    else:
        form = DrinkForm()
    return render(request, 'mealtracker/drink_form.html', {'form': form})

@login_required
def drink_update(request, pk):
    drink = Drink.objects.get(pk=pk)
    form = DrinkForm(request.POST or None, request.FILES or None, instance=drink)
    if form.is_valid():
        form.save()
        return redirect('mealtracker:drink_list')
    return render(request, 'mealtracker/drink_form.html', {'form': form})

@login_required
def drink_delete(request, pk):
    drink = Drink.objects.get(pk=pk)
    if request.method == 'POST':
        drink.delete()
        return redirect('mealtracker:drink_list')
    return render(request, 'mealtracker/drink_confirm_delete.html', {'drink': drink})

#diettype
@login_required
def diettype_list(request):
    diettypes = DietType.objects.all()
    return render(request, 'mealtracker/diettype_list.html', {'diettypes': diettypes})

@login_required
def diettype_create(request):
    if request.method == 'POST':
        form = DietTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:diettype_list')
    else:
        form = DietTypeForm()
    return render(request, 'mealtracker/diettype_form.html', {'form': form})

@login_required
def diettype_update(request, pk):
    diettype = get_object_or_404(DietType, pk=pk)
    form = DietTypeForm(request.POST or None, instance=diettype)
    if form.is_valid():
        form.save()
        return redirect('mealtracker:diettype_list')
    return render(request, 'mealtracker/diettype_form.html', {'form': form})

@login_required
def diettype_delete(request, pk):
    diettype = get_object_or_404(DietType, pk=pk)
    if request.method == 'POST':
        diettype.delete()
        return redirect('mealtracker:diettype_list')
    return render(request, 'mealtracker/diettype_confirm_delete.html', {'diettype': diettype})

#avoiditem
@login_required
def avoiditem_list(request):
    items = AvoidItem.objects.all()
    return render(request, 'avoiditem/avoiditem_list.html', {'items': items})

@login_required
def avoiditem_create(request):
    if request.method == 'POST':
        form = AvoidItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:avoiditem_list')
    else:
        form = AvoidItemForm()
    return render(request, 'avoiditem/avoiditem_form.html', {'form': form})

@login_required
def avoiditem_update(request, pk):
    item = get_object_or_404(AvoidItem, pk=pk)
    if request.method == 'POST':
        form = AvoidItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:avoiditem_list')
    else:
        form = AvoidItemForm(instance=item)
    return render(request, 'avoiditem/avoiditem_form.html', {'form': form})

@login_required
def avoiditem_delete(request, pk):
    item = get_object_or_404(AvoidItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('mealtracker:avoiditem_list')
    return render(request, 'avoiditem/avoiditem_confirm_delete.html', {'item': item})

#supplement
@login_required
def supplement_list(request):
    supplements = Supplement.objects.all()
    return render(request, 'supplement/supplement_list.html', {'supplements': supplements})

@login_required
def supplement_create(request):
    if request.method == 'POST':
        form = SupplementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:supplement_list')
    else:
        form = SupplementForm()
    return render(request, 'supplement/supplement_form.html', {'form': form})

@login_required
def supplement_update(request, pk):
    supplement = get_object_or_404(Supplement, pk=pk)
    if request.method == 'POST':
        form = SupplementForm(request.POST, request.FILES, instance=supplement)
        if form.is_valid():
            form.save()
            return redirect('mealtracker:supplement_list')
    else:
        form = SupplementForm(instance=supplement)
    return render(request, 'supplement/supplement_form.html', {'form': form})

@login_required
def supplement_delete(request, pk):
    supplement = get_object_or_404(Supplement, pk=pk)
    if request.method == 'POST':
        supplement.delete()
        return redirect('mealtracker:supplement_list')
    return render(request, 'supplement/supplement_confirm_delete.html', {'supplement': supplement})