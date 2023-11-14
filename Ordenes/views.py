from django.shortcuts import render, HttpResponse, redirect
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from .Carrito import Carrito
from DataAccess import forms, models


def tienda(request, rest):
    """
    Maneja la creación de pedidos en la tienda de un restaurante y el envío de confirmaciones por correo electrónico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante para filtrar la base de datos.

    Returns:
        HttpResponse: Una página renderizada o una redirección dependiendo de la solicitud HTTP.
    """

    # Obtener el restaurante y preparar variables
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    hora = datetime.now()

    # Generar identificador único para el pedido basado en fecha, hora y contenido del carrito
    fecha_hora_actual_str = (f"{hora.year}{hora.month:02d}{hora.day:02d}"
                             f"{hora.hour:02d}{hora.minute:02d}{hora.second:02d}{len(carrito.carrito)}")

    # Preparar la forma para elegir mesa si es una solicitud GET
    num_choices = restau[0].cantidadMesas  # Ajusta este valor según tus necesidades
    if request.method == 'GET':
        form = forms.MesaForm(num_choices)
        platos = models.plato.objects.filter(restaurante=restau[0])
        inven = models.inventario.objects.all()
        estaciones = set(pla.estacion for pla in platos)

        context = {
            'restaurante': restau[0],
            'estaciones': estaciones,
            'platos': platos,
            'inventario': inven,
            'form': form
        }
        return render(request, 'Ordenes/tienda.html', context)

    # Manejar la solicitud POST: procesar pedido y enviar correo electrónico
    elif request.method == 'POST':
        form = forms.MesaForm(num_choices, request.POST)
        if not form.is_valid():
            # Manejar formulario no válido aquí, p.ej., volver a renderizar con errores
            return render(request, 'error.html', {'form': form})

        # Procesamiento del pedido
        numero, correo = form.cleaned_data['numero'], form.cleaned_data['correo']
        newOrden = models.factura(restaurante=restau[0], email=correo, identificatorOrder=fecha_hora_actual_str)
        newOrden.save()

        total, platos, cantidades, totalPlato = procesar_carrito(carrito, restau, newOrden, numero, hora)

        # Preparar y enviar correo electrónico
        enviar_confirmacion_por_correo(correo, restau, platos, cantidades, total, totalPlato, fecha_hora_actual_str)

        # Redirigir a la página de detalles del pedido
        return redirect('OrderDetails', rest, fecha_hora_actual_str)

def procesar_carrito(carrito, restau, newOrden, numero, hora):
    """
    Procesa los artículos en el carrito, actualiza el inventario y crea órdenes.

    Args:
        carrito: Objeto Carrito conteniendo los productos seleccionados.
        restau: Objeto restaurante para el que se realiza el pedido.
        newOrden: Objeto factura para asociar con las órdenes.
        numero: Número de mesa elegido para el pedido.
        hora: Objeto datetime representando la hora actual.

    Returns:
        tuple: Total del pedido, listas de platos, cantidades y totales por plato.
    """
    platos, cantidades, totalPlato = [], [], []
    total = 0.0

    for plato in carrito.carrito.values():
        plato_id, cantidad, acumulado = plato['producto_id'], plato['cantidad'], plato['acumulado']
        plato_obj = models.plato.objects.get(id=plato_id)
        platos.append(plato_obj)
        cantidades.append(cantidad)
        total += plato_obj.precio * cantidad
        totalPlato.append(str(acumulado))

        # Actualización del inventario
        for inv in models.inventario.objects.filter(restaurante=restau[0], plato=plato_obj):
            if inv.producto:
                nuevaDisponibilidad = max(inv.producto.cantidadDisponible - inv.cantidadGastada, 0)
                inv.producto.cantidadDisponible = nuevaDisponibilidad
                inv.producto.save()

        # Crear orden para cada plato en el carrito
        models.orden.objects.create(
            restaurante=restau[0], plato=plato_obj, mesa=numero,
            cantidad=cantidad, horaPedido=hora, identificator=newOrden.identificatorOrder
        )

    # Limpiar carrito después de procesar
    carrito.limpiar()

    return total, platos, cantidades, totalPlato

def enviar_confirmacion_por_correo(correo, restau, platos, cantidades, total, totalPlato, fecha_hora_actual_str):
    """
    Prepara y envía un correo electrónico de confirmación del pedido.

    Args:
        correo: Correo electrónico del destinatario.
        restau: Objeto restaurante asociado al pedido.
        platos: Lista de platos pedidos.
        cantidades: Cantidad de cada plato pedido.
        total: Total del pedido.
        totalPlato: Total acumulado de cada plato.
        fecha_hora_actual_str: Identificador único del pedido.

    Returns:
        None
    """
    # Preparar el contexto para renderizar la plantilla de correo
    context = {
        'restaurante': restau[0],
        'platos': platos,
        'cantidades': cantidades,
        'total': total,
        'tam': range(len(platos)),
        'totalPlato': totalPlato,
        'id': fecha_hora_actual_str
    }
    html_content = render_to_string("Factura/factura.html", context)
    text_content = strip_tags(html_content)

    # Configurar y enviar correo electrónico
    subject = f'Confirmacion orden {fecha_hora_actual_str}'
    from_email = 'dikkatrc@gmail.com'
    email = EmailMultiAlternatives(subject, text_content, from_email, [correo])
    email.attach_alternative(html_content, "text/html")
    email.send()


def orderDetails(request, rest, identificator):
    """
    Muestra los detalles de un pedido específico en un restaurante.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        identificator: str, el identificador único del pedido.

    Returns:
        HttpResponse: Renderiza la página de detalles del pedido con el contexto apropiado.
    """

    # Obtener el restaurante y las órdenes asociadas con el identificador
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(identificator=identificator)

    # Preparar listas para platos, cantidades y estado de pago
    platos, cantidades, pagados = [], [], []
    for order in orders:
        platos.append(order.plato)
        cantidades.append(order.cantidad)
        pagados.append(order.pagado)

    # Determinar si la orden ha sido completamente pagada
    pagaCompleta = all(pagados)

    # Preparar otros elementos del contexto
    inven = models.inventario.objects.all()
    estaciones = []  # Aquí puedes agregar lógica para determinar estaciones si es necesario
    tamano = len(orders)

    # Configurar el contexto para la plantilla
    context = {
        'restaurante': restau[0],
        'estaciones': estaciones,
        'especiales': platos,
        'inventario': inven,
        'cantidades': cantidades,
        'pagados': pagados,
        'tamano': tamano,
        'estado': orders[0].estado if orders else None,
        'identificator': identificator,
        'pagaCompleta': pagaCompleta,
        'form': forms.pagoForm(request.POST) if request.method == 'POST' else forms.pagoForm()
    }

    return render(request, 'Ordenes/orderDetails.html', context)


def ordenes(request, rest):
    """
    Muestra las órdenes activas de un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante para filtrar las órdenes.

    Returns:
        HttpResponse: Una página renderizada con los detalles de las órdenes del restaurante.
    """

    # Obtener el restaurante y las órdenes activas
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], estado=True)

    # Recolectar mesas únicas de las órdenes
    mesas = list(set(order.mesa for order in orders))

    # Preparar el formulario, se asume que es necesario solo para solicitudes POST
    form = forms.pagoForm(request.POST) if request.method == 'POST' else forms.pagoForm()

    # Configurar el contexto para la plantilla
    context = {
        'restaurante': restau[0],
        'ordenes': orders,
        'mesas': mesas,
        'isPay': False,  # Asumiendo que 'isPay' se refiere a si se ha realizado un pago
        'form': form
    }

    return render(request, 'Ordenes/ordenes.html', context)


def ordenesPagar(request, rest):
    """
    Muestra las órdenes que están pendientes de pago en un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante para filtrar las órdenes.

    Returns:
        HttpResponse: Una página renderizada con los detalles de las órdenes pendientes de pago del restaurante.
    """

    # Obtener el restaurante y las órdenes pendientes de pago
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], pagado=False, estado=False)

    # Recolectar mesas únicas de las órdenes
    mesas = list(set(order.mesa for order in orders))

    # Preparar el formulario, se asume que es necesario solo para solicitudes POST
    form = forms.pagoForm(request.POST) if request.method == 'POST' else forms.pagoForm()

    # Configurar el contexto para la plantilla
    context = {
        'restaurante': restau[0],
        'ordenes': orders,
        'mesas': mesas,
        'isPay': True,  # Indica que la página está relacionada con el proceso de pago
        'form': form
    }

    return render(request, 'Ordenes/ordenes.html', context)


def entregarMesa(request, rest, mesa):
    """
    Marca todas las órdenes en una mesa específica como entregadas.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        mesa: str, el número de la mesa.

    Returns:
        HttpResponse: Redirección a la página de órdenes del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], estado=True)
    for pla in orders:
        if pla.mesa == int(mesa):
            pla.estado = False
            pla.save()

    return redirect('Ordenes', rest)


def entregarOrden(request, rest, identificator):
    """
    Marca toda la órden como entregadas.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        mesa: str, el número de la mesa.

    Returns:
        HttpResponse: Redirección a la página de órdenes del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(identificator=identificator)
    for pla in orders:
        if pla.identificator == identificator:
            pla.estado = False
            pla.save()

    return redirect('Ordenes', rest)

def pagarPlato(request, rest, identificator, plato):
     """
    Marca un plato específico en una orden como pagado.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        identificator: str, el identificador de la orden.
        plato: str, el nombre del plato.

    Returns:
        HttpResponse: Redirección a la página de detalles de la orden.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    plat = models.plato.objects.get(nombre=plato, restaurante=restau[0])
    orders = models.orden.objects.filter(identificator=identificator, plato=plat)
    for pla in orders:
        if pla.identificator == identificator:
            pla.pagado = True
            pla.save()

    return redirect('OrderDetails', rest, identificator)

def pagarOrden(request, rest, identificator):
    """
    Marca todas las órdenes con un identificador específico como pagadas.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        identificator: str, el identificador de la orden.

    Returns:
        HttpResponse: Redirección a la página de detalles de la orden.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(identificator=identificator)
    for pla in orders:
        if pla.identificator == identificator:
            pla.pagado = True
            pla.save()

    return redirect('OrderDetails', rest, identificator)


def pagarMesa(request, rest, mesa):
    """
    Marca todas las órdenes en una mesa específica como pagadas.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        mesa: str, el número de la mesa.

    Returns:
        HttpResponse: Redirección a la página de órdenes pendientes de pago.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    orders = models.orden.objects.filter(restaurante=restau[0], estado=False)
    for pla in orders:
        if pla.mesa == int(mesa):
            pla.pagado = True
            pla.save()

    return redirect('ordenesPagar', rest)


def agregar_producto(request, rest, producto_id):
    """
    Agrega un producto al carrito de compras.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        producto_id: int, el identificador del producto a agregar.

    Returns:
        HttpResponse: Redirección a la tienda del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    producto = models.plato.objects.get(id=producto_id)
    carrito.agregar(producto)
    return redirect("Tienda", rest)


def eliminar_producto(request, rest, producto_id):
    """
    Elimina un producto al carrito de compras.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        producto_id: int, el identificador del producto a agregar.

    Returns:
        HttpResponse: Redirección a la tienda del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    producto = models.plato.objects.get(id=producto_id)
    carrito.eliminar(producto)
    return redirect("Tienda", rest)


def restar_producto(request, rest, producto_id):
    """
    Resta la cantidad pedida un producto al carrito de compras.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        producto_id: int, el identificador del producto a agregar.

    Returns:
        HttpResponse: Redirección a la tienda del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest)
    carrito = Carrito(request)
    producto = models.plato.objects.get(id=producto_id)
    carrito.restar(producto)
    return redirect("Tienda", rest)


def limpiar_carrito(request, rest):
    """
    Limpia al carrito de compras.

    Args:
        request: HttpRequest, la solicitud HTTP.
        rest: str, el nombre del restaurante.
        producto_id: int, el identificador del producto a agregar.

    Returns:
        HttpResponse: Redirección a la tienda del restaurante.
    """
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
                print("Entro")
                for inv in inventario:
                    print(inv)
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
