from django.urls import path

from . import views

urlpatterns = [
    path('<str:rest>/registro', views.register, name='registro'),
    path('<str:rest>/team', views.team, name='team'),
    path('', views.inicio, name='inicio'),
    path('dikkat/login', views.loginView, name='login'),
    path('dikkat/logout/<str:rest>', views.salir, name='logout'),
]