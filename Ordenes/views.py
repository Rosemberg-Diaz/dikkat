from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from .Carrito import Carrito
from DataAccess import forms, models


def tienda(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    hora = datetime.now()
    hora_actual = str(hora.hour)
    minuto_actual = str(hora.minute)
    segundo_actual = str(hora.second)
    anio_actual = str(hora.year)
    mes_actual = str(hora.month)
    dia_actual = str(hora.day)
    fecha_hora_actual_str = anio_actual + mes_actual + dia_actual + hora_actual + minuto_actual + segundo_actual + str(
        len(carrito.carrito))
    platos = []
    cantidades = []
    totalPlato = []
    total = 0.0
    num_choices = restau[0].cantidadMesas  # Cambia este valor según tus necesidades
    if request.method == 'POST':

        form = forms.MesaForm(num_choices, request.POST)
        if form.is_valid():
            # Procesa los datos del formulario aquí
            numero = form.cleaned_data['numero']
            correo = form.cleaned_data['correo']
            newOrden = models.factura(restaurante=restau[0], email=correo, identificatorOrder=fecha_hora_actual_str)
            newOrden.save()
            for plato in carrito.carrito:
                print(plato)
                plato_idSto = carrito.carrito[plato]["producto_id"]
                cantidadSto = carrito.carrito[plato]["cantidad"]
                acumuladoSto = carrito.carrito[plato]["acumulado"]
                plato = models.plato.objects.get(id=plato_idSto)
                platos.append(plato)
                cantidades.append(cantidadSto)
                total = total + (plato.precio * cantidadSto)
                totalPlato.append(str(acumuladoSto))
                newOrden = models.orden(restaurante=restau[0], plato=plato, mesa=numero, cantidad=cantidadSto,
                                        horaPedido=hora, identificator=fecha_hora_actual_str)
                newOrden.save()
            carrito.limpiar()

            # Datos que deseas pasar a la plantilla (contexto)
            tam = range(len(platos))
            context = {
                'restaurante': restau[0],
                'platos': platos,
                'cantidades': cantidades,
                'total': total,
                'tam': tam,
                'totalPlato': totalPlato,
                'id': fecha_hora_actual_str
            }

            # Renderiza la plantilla HTML a una cadena
            html_content = render_to_string("Factura/factura.html", context)

            # Renderiza la versión de texto sin formato del correo
            text_content = strip_tags(html_content)

            # Configura el correo electrónico
            subject = 'Confirmacion orden ' + fecha_hora_actual_str
            from_email = 'dikkatrc@gmail.com'
            recipient_list = [correo]

            # Crea un objeto EmailMessage
            email = EmailMessage(subject, strip_tags(html_content), from_email, recipient_list)

            # Crea un objeto EmailMultiAlternatives
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)

            # Adjunta la versión HTML de la plantilla
            email.attach_alternative(html_content, "text/html")
            # Envía el correo electrónico
            email.send()
            return redirect('OrderDetails', rest, fecha_hora_actual_str)
    else:
        form = forms.MesaForm(num_choices)
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
        'inventario': inven,
        'form': form
    }

    return render(request, 'Ordenes/tienda.html', context)


def orderDetails(request, rest, identificator):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(identificator=identificator)
    platos = []
    cantidades = []
    pagados = []
    form = forms.pagoForm(request.POST)
    pagaCompleta = False
    for order in orders:
        platos.append(order.plato)
        cantidades.append(order.cantidad)
        pagados.append(order.pagado)
    if all(valor == True for valor in pagados):
        pagaCompleta = True
    else:
        pagaCompleta = False

    inven = models.inventario.objects.all()
    estaciones = []
    tamano = range(len(orders))
    context = {
        'restaurante': restau[0],
        'estaciones': estaciones,
        'especiales': platos,
        'inventario': inven,
        'cantidades': cantidades,
        'pagados': pagados,
        'tamano': tamano,
        'estado': orders[0].estado,
        'identificator': identificator,
        'pagaCompleta': pagaCompleta,
        'form': form
    }
    return render(request, 'Ordenes/orderDetails.html', context)


def ordenes(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], estado=True)
    ordenes = []
    mesas = []
    form = forms.pagoForm(request.POST)
    for pla in orders:
        if pla.mesa not in mesas:
            mesas.append(pla.mesa)

    if orders:
        context = {
            'restaurante': restau[0],
            'ordenes': orders,
            'mesas': mesas,
            'estado': orders[0].estado,
            'isPay':False,
            'form':form
        }
    else:
        context = {
            'restaurante': restau[0],
            'ordenes': orders,
            'mesas': mesas,
            'isPay':False,
            'form':form
        }
    return render(request, 'Ordenes/ordenes.html', context)


def ordenesPagar(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], pagado=False, estado=False)
    ordenes = []
    mesas = []
    form = forms.pagoForm(request.POST)
    for pla in orders:
        if pla.mesa not in mesas:
            mesas.append(pla.mesa)

    if orders:
        context = {
            'restaurante': restau[0],
            'ordenes': orders,
            'mesas': mesas,
            'estado': orders[0].estado,
            'isPay':True,
            'form':form
        }
    else:
        context = {
            'restaurante': restau[0],
            'ordenes': orders,
            'mesas': mesas,
            'isPay':True,
            'form':form
        }
    return render(request, 'Ordenes/ordenes.html', context)


def entregarMesa(request, rest, mesa):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], estado=True)
    for pla in orders:
        print(pla.mesa)
        if pla.mesa == int(mesa):
            print(pla)
            pla.estado = False
            pla.save()

    return redirect('Ordenes', rest)


def entregarOrden(request, rest, identificator):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(identificator=identificator)
    for pla in orders:
        if pla.identificator == identificator:
            print(pla)
            pla.estado = False
            pla.save()

    return redirect('Ordenes', rest)

def pagarPlato(request, rest, identificator, plato):
    restau = models.restaurante.objects.filter(nombre=rest)
    plat = models.plato.objects.get(nombre=plato, restaurante=restau[0])
    orders = models.orden.objects.filter(identificator=identificator, plato=plat)
    for pla in orders:
        if pla.identificator == identificator:
            pla.pagado = True
            pla.save()

    return redirect('OrderDetails', rest, identificator)

def pagarOrden(request, rest, identificator):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(identificator=identificator)
    for pla in orders:
        if pla.identificator == identificator:
            pla.pagado = True
            pla.save()

    return redirect('OrderDetails', rest, identificator)


def pagarMesa(request, rest, mesa):
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], estado=False)
    for pla in orders:
        if pla.mesa == int(mesa):
            pla.pagado = True
            pla.save()

    return redirect('ordenesPagar', rest)


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
    hora = datetime.now()
    hora_actual = str(hora.hour)
    minuto_actual = str(hora.minute)
    segundo_actual = str(hora.second)
    anio_actual = str(hora.year)
    mes_actual = str(hora.month)
    dia_actual = str(hora.day)
    fecha_hora_actual_str = anio_actual + mes_actual + dia_actual + hora_actual + minuto_actual + segundo_actual + str(
        len(carrito.carrito))
    platos = []
    cantidades = []
    totalPlato = []
    total = 0.0
    num_choices = restau[0].cantidadMesas  # Cambia este valor según tus necesidades
    if request.method == 'POST':
        form = forms.CorreoForm(num_choices, request.POST)
        if form.is_valid():
            # Procesa los datos del formulario aquí
            correo = form.cleaned_data['correo']
            numero = form.cleaned_data['numero']
            for plato in carrito.carrito:
                plato_idSto = carrito.carrito[plato]["producto_id"]
                cantidadSto = carrito.carrito[plato]["cantidad"]
                acumuladoSto = carrito.carrito[plato]["acumulado"]
                plato = models.plato.objects.get(id=plato_idSto)
                platos.append(plato)
                cantidades.append(cantidadSto)
                total = total + (plato.precio * cantidadSto)
                inventario = models.inventario.objects.filter(restaurante=restau[0],plato=plato)
                for inv in inventario:
                    if(inv.producto):
                        producto = inv.producto
                        nuevaDisponibilidad = producto.cantidadDisponible - inv.cantidadGastada
                        if(nuevaDisponibilidad<0):
                            producto.cantidadDisponible = 0
                        else:
                            producto.cantidadDisponible = producto.cantidadDisponible - inv.cantidadGastada
                        producto.save()
                totalPlato.append(str(acumuladoSto))
                newOrden = models.orden(restaurante=restau[0], plato=plato, mesa=numero, cantidad=cantidadSto,
                                        horaPedido=hora, identificator=fecha_hora_actual_str)
                newOrden.save()
            carrito.limpiar()
            # Datos que deseas pasar a la plantilla (contexto)
            tam = range(len(platos))
            context = {
                'restaurante': restau[0],
                'platos': platos,
                'cantidades': cantidades,
                'total': total,
                'tam': tam,
                'totalPlato': totalPlato
            }

            # Renderiza la plantilla HTML a una cadena
            html_content = render_to_string("Factura/factura.html", context)

            # Renderiza la versión de texto sin formato del correo
            text_content = strip_tags(html_content)

            # Configura el correo electrónico
            subject = 'Asunto del correo'
            from_email = 'dikkatrc@gmail.com'
            recipient_list = [correo]

            # Crea un objeto EmailMultiAlternatives
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)

            # Adjunta la versión HTML de la plantilla
            email.attach_alternative(html_content, "text/html")
            # Envía el correo electrónico
            email.send()
    else:
        form = forms.CorreoForm(num_choices)
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
        'inventario': inven,
        'form': form
    }

    return render(request, 'Ordenes/tienda.html', context)
