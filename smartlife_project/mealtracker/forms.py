from django import forms
from .models import Meal
from .models import Drink
from .models import DietType
from .models import AvoidItem
from .models import Supplement

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'category', 'calories', 'protein', 'image']

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name', 'category', 'calories', 'sugar', 'image']

class DietTypeForm(forms.ModelForm):
    class Meta:
        model = DietType
        fields = '__all__'

class AvoidItemForm(forms.ModelForm):
    class Meta:
        model = AvoidItem
        fields = ['name', 'reason', 'severity', 'image', 'notes']

class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = ['name', 'brand', 'benefits', 'dosage', 'image']