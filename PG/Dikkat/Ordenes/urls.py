from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('<str:rest>/ordenar', views.tienda, name="Tienda"),
    path('<str:rest>/ordenar/agregar/<int:producto_id>/', views.agregar_producto, name="Add"),
    path('<str:rest>/ordenar/eliminar/<int:producto_id>/', views.eliminar_producto, name="Del"),
    path('<str:rest>/ordenar/restar/<int:producto_id>/', views.restar_producto, name="Sub"),
    path('<str:rest>/ordenar/limpiar/', views.limpiar_carrito, name="CLS"),
    path('<str:rest>/crearOrden', views.crear_orden, name="CrearOrden"),
]