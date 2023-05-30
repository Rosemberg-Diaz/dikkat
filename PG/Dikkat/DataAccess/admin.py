from django.contrib import admin

# Register your models here.
from .models import proveedor, plato, producto, User, restaurante


admin.site.register(restaurante)
admin.site.register(plato)
admin.site.register(producto)
admin.site.register(User)
