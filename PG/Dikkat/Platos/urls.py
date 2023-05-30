from django.urls import path

from . import views

urlpatterns = [
    path('<str:rest>/crearProducto', views.crearPro, name='crearPro'),
    path('<str:rest>/crearPlato', views.crearPla, name='crearPla'),
    path('<str:rest>/productos', views.products, name='productos'),
    path('<str:rest>/<str:pla>/añadirProducto', views.proByPla, name='añadirPro'),
    path('<str:rest>/<str:plat>/editarPlato', views.editarPla, name='editarPla'),
    path('<str:rest>/<str:pro>/editarProducto', views.editarPro, name='editarPro'),
]