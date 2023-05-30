from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DataAccess.urls')),
    path('', include('Usuarios.urls')),
    path('', include('Restaurantes.urls')),
    path('', include('Platos.urls')),
    path('', include('Ordenes.urls')),
]
