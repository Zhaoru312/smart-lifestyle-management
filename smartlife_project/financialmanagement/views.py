from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget, Expense, Income, Category, FinancialGoal
from .forms import BudgetForm, ExpenseForm, IncomeForm, CategoryForm, FinancialGoalForm
from django.contrib.auth.decorators import login_required

#dashboard
@login_required
def financial_home(request):
    # Calculate totals
    total_income = sum(income.amount for income in Income.objects.all())
    total_expense = sum(expense.amount for expense in Expense.objects.all())
    total_balance = total_income - total_expense
    
    # Get recent budgets (up to 5)
    budgets = Budget.objects.all()[:5]
    
    # Calculate budget usage percentage (simplified example)
    total_budget = sum(budget.amount for budget in Budget.objects.all())
    total_used = sum(expense.amount for expense in Expense.objects.all())
    budget_usage = (total_used / total_budget * 100) if total_budget > 0 else 0
    
    # Get financial goals
    financial_goals = FinancialGoal.objects.all()
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'total_balance': total_balance,
        'budgets': budgets,
        'budget_usage': round(budget_usage, 2),
        'financial_goals': financial_goals,
    }
    
    return render(request, 'financialmanagement/index.html', context)

#budget
@login_required
def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, 'financialmanagement/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm()
    return render(request, 'financialmanagement/budget_form.html', {'form': form})

@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'financialmanagement/budget_form.html', {'form': form})

@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        budget.delete()
        return redirect('budget_list')
    return render(request, 'financialmanagement/budget_confirm_delete.html', {'budget': budget})

#expense
@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'financialmanagement/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'financialmanagement/expense_form.html', {'form': form})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'financialmanagement/expense_form.html', {'form': form})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'financialmanagement/expense_confirm_delete.html', {'expense': expense})

#income
@login_required
def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('income_list')  
    else:
        form = IncomeForm()
    return render(request, 'financialmanagement/income_form.html', {'form': form})

@login_required
def income_list(request):
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'financialmanagement/income_list.html', {'incomes': incomes})

@login_required
def income_edit(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'financialmanagement/income_form.html', {'form': form, 'title': 'Edit Income'})

@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'financialmanagement/income_confirm_delete.html', {'income': income})

#category
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'financialmanagement/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'financialmanagement/category_form.html', {'form': form})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'financialmanagement/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'financialmanagement/category_confirm_delete.html', {'category': category})

#financial
@login_required
def financial_goal_list(request):
    goals = FinancialGoal.objects.all()
    return render(request, 'financialmanagement/financial_goal_list.html', {'goals': goals})

@login_required
def financial_goal_create(request):
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('financialgoal_list')
    else:
        form = FinancialGoalForm()
    return render(request, 'financialmanagement/financial_goal_form.html', {'form': form})

@login_required
def financial_goal_edit(request, pk):
    goal = get_object_or_404(FinancialGoal, pk=pk)
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('financialgoal_list')
    else:
        form = FinancialGoalForm(instance=goal)
    return render(request, 'financialmanagement/financial_goal_form.html', {'form': form})

@login_required
def financial_goal_delete(request, pk):
    goal = get_object_or_404(FinancialGoal, pk=pk)
    if request.method == 'POST':
        goal.delete()
        return redirect('financialgoal_list')
    return render(request, 'financialmanagement/financial_goal_confirm_delete.html', {'goal': goal})