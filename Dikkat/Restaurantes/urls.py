from django.urls import path

from . import views

urlpatterns = [
    path('<str:rest>/inicio', views.dikkat, name='inicio'),
    path('<str:rest>/restaurante', views.restauranteView, name='restaurant'),
    path('<str:rest>/menu', views.menu, name='menu'),
    path('<str:rest>/especiales', views.especiales, name='especiales'),
    path('<str:rest>/editarRestaurante', views.editarRest, name='editarRest'),
    path('administrador/crearRestaurante', views.crearRest, name='crearRest'),
    ]