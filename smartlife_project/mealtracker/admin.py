from django.contrib import admin
from .models import Meal, Category
from .models import Drink
from .models import DietType
from .models import AvoidItem
from .models import Supplement

admin.site.register(Drink)
admin.site.register(Meal)
admin.site.register(Category)
admin.site.register(DietType)
admin.site.register(AvoidItem)
admin.site.register(Supplement)