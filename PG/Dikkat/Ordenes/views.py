from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

# Create your views here.
from .Carrito import Carrito
from DataAccess import forms, models


def tienda(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    platos = models.plato.objects.filter(restaurante=restau[0])
    inven = models.inventario.objects.all()
    estaciones = []

    for pla in platos:
        if pla.estacion not in estaciones:
            estaciones.append(pla.estacion)
    context = {
        'restaurante': restau[0],
        'estaciones': estaciones,
        'platos': platos,
        'inventario': inven
    }
    return render(request, "Ordenes/tienda.html", context)

def agregar_producto(request, rest, producto_id):
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    producto = models.plato.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("Tienda", rest)

def eliminar_producto(request, rest, producto_id):
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    producto = models.plato.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Tienda", rest)

def restar_producto(request, rest, producto_id):
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    producto = models.plato.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda", rest)

def limpiar_carrito(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("Tienda", rest)

def crear_orden(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    plato_idSto = ""
    nombreSto = ""
    precioSto = ""
    acumuladoSto = ""
    cantidadSto = ""
    hora= datetime.now()
    print("Carrito",type(carrito.carrito))
    for plato in carrito.carrito:
        plato_idSto = carrito.carrito[plato]["producto_id"]
        cantidadSto = carrito.carrito[plato]["cantidad"]
        plato = models.plato.objects.get(id=plato_idSto)
        newOrden = models.orden(restaurante=restau[0], plato=plato, mesa=1, cantidad=cantidadSto, horaPedido=hora)
        newOrden.save()
    carrito.limpiar()
    return redirect("Tienda", rest)