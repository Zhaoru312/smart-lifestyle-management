from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    calories = models.FloatField()
    protein = models.FloatField()
    image = models.ImageField(upload_to='meal_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Drink(models.Model):
    name = models.CharField(max_length=100)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    calories = models.FloatField()            
    sugar = models.FloatField()              
    is_caffeinated = models.BooleanField(default=False)    
    image = models.ImageField(upload_to='drink_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class DietType(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True, null=True) 
    recommended_calories = models.IntegerField(blank=True, null=True)  
    suitable_for = models.CharField(max_length=200, blank=True, null=True)  
    not_suitable_for = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return self.name

class AvoidItem(models.Model):
    name = models.CharField(max_length=100)
    reason = models.TextField()
    severity_choices = [
        (1, 'Low'),
        (2, 'Moderate'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    severity = models.IntegerField(choices=severity_choices, null=True, blank=True)
    image = models.ImageField(upload_to='avoid_items/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Supplement(models.Model):
    name = models.CharField(max_length=100)          
    brand = models.CharField(max_length=100, blank=True, null=True)  
    benefits = models.TextField(blank=True, null=True) 
    dosage = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='supplement_images/', blank=True, null=True)

    def __str__(self):
        return self.name
