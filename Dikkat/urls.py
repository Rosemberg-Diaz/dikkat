from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DataAccess.urls')),
    path('', include('Usuarios.urls')),
    path('', include('Restaurantes.urls')),
    path('', include('Platos.urls')),
    path('', include('Ordenes.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
