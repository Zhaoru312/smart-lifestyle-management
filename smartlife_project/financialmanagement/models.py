from django.db import models

class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"
    
class Income(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=[('income', 'Income'), ('expense', 'Expense')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FinancialGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('saving', 'Tabungan'),
        ('investment', 'Investasi'),
        ('purchase', 'Pembelian'),
        ('debt', 'Pembayaran Utang'),
        ('other', 'Lainnya'),
    ]

    name = models.CharField(max_length=100)
    target_amount = models.PositiveIntegerField()
    current_amount = models.PositiveIntegerField(default=0)
    due_date = models.DateField()
    type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name