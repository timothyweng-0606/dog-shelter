from django.contrib import admin

# Register your models here.
from .models import Dog, Vacination

admin.site.register(Dog)
admin.site.register(Vacination)