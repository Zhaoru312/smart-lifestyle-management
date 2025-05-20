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
