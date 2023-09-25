from django.contrib import admin

# Register your models here.
from .models import plato, producto, User, restaurante


admin.site.register(restaurante)
admin.site.register(plato)
admin.site.register(producto)
admin.site.register(User)
