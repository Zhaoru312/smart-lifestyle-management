from django.contrib import admin
from .models import Feature, Testimonial, FAQ, ContactMessage, HeroSection

# Register your models here.

admin.site.register(Feature)
admin.site.register(Testimonial)
admin.site.register(FAQ)
admin.site.register(ContactMessage)
admin.site.register(HeroSection)
