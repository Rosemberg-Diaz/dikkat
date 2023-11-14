from django.shortcuts import render, redirect
from DataAccess import forms, models
import base64

def encode_file(nombre):
    """
        Codifica el contenido de un archivo en una cadena base64.

        Args:
            file_object: Un objeto de archivo que será leído y codificado.

        Returns:
            str: Una cadena de texto que representa el contenido del archivo en formato base64.
        """
    image_read = nombre.read()
    encoded_bytes = base64.b64encode(image_read)
    encoded_string = encoded_bytes.decode('utf-8')
    return (encoded_string)

def products(request, rest):
    """
        Muestra los productos disponibles en un restaurante específico.

        Args:
            request: HttpRequest que contiene los datos de la solicitud.
            rest: Nombre del restaurante para filtrar los productos.

        Returns:
            HttpResponse: Una página renderizada con los productos del restaurante.
        """
    restau = models.restaurante.objects.filter(nombre=rest)
    productos = models.producto.objects.filter(restaurante=restau[0])

    context = {
        'restaurante': restau[0],
        'productos': productos,
    }
    return render(request, 'Platos/productos.html', context)


def proByPla(request, rest, pla):
    """
        Maneja la visualización y gestión de productos asociados a un plato específico en un restaurante.

        Args:
            request: HttpRequest que contiene los datos de la solicitud.
            rest: Nombre del restaurante.
            pla: Nombre del plato.

        Returns:
            HttpResponse: Una página renderizada con productos asociados al plato o una redirección tras una acción exitosa.
        """
    restau = models.restaurante.objects.filter(nombre=rest)
    products = models.producto.objects.filter(restaurante=restau[0])
    plat = models.plato.objects.filter(nombre=pla)
    inv = models.inventario.objects.filter(restaurante=restau[0], plato=plat[0])
    if len(products) == 0:
        products = 0
    if request.method == 'POST':
        details = forms.productPlatoForm(request.POST)
        if details.is_valid():
            post = details.save(commit=False)
            # Finally write the changes into database
            post.save()
            prod = models.producto.objects.filter(restaurante=restau[0], nombre=request.POST['producto'])
            p = models.inventario.objects.get(producto=None, restaurante=None, plato=None, cantidadGastada=request.POST['cantidadGastada'])
            p.producto = prod[0]
            p.restaurante = restau[0]
            p.plato = plat[0]
            p.save()
            return redirect('añadirPro', rest, pla)
        else:
            if len(inv) > 0:
                context = {
                    'restaurante': restau[0],
                    'plato': plat[0],
                    'inventario': inv,
                    'form': details,
                    'productos': products
                }
            else:
                context = {
                    'restaurante': restau[0],
                    'plato': plat[0],
                    'error': 'No se encontraron producto asociados',
                    'form': details,
                    'productos': products
                }
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "Platos/productosByPlatos.html", context)
    else:
        form = forms.productPlatoForm(None)
        if len(inv) > 0:
            context = {
                'restaurante': restau[0],
                'plato': plat[0],
                'inventario': inv,
                'form': form,
                'productos': products
            }
        else:
            context = {
                'restaurante': restau[0],
                'plato': plat[0],
                'error': 'No se encontraron producto asociados',
                'form': form,
                'productos': products
            }
        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page

        return render(request, 'Platos/productosByPlatos.html', context)

def crearPro(request, rest):
    """
    Gestiona la creación de un nuevo producto para un restaurante específico.
    Muestra un formulario para añadir un producto y procesa la información enviada.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante para el cual se crea el producto.

    Returns:
        HttpResponse: Renderiza la página del formulario o redirige tras una acción exitosa.
    """

    # Obtener el restaurante por su nombre
    restau = models.restaurante.objects.filter(nombre=rest).first()

    if request.method == 'POST':
        details = forms.productoForm(request.POST)

        if details.is_valid():
            post = details.save(commit=False)
            post.restaurante = restau
            # Llamada a la función para codificar la imagen
            if 'uploadFromPC' in request.FILES:
                imagen = encode_file(request.FILES['uploadFromPC'])
                post.imagenInv = imagen
            post.save()
            return redirect('productos', rest)
        else:
            return render(request, "Platos/crearProducto.html", {'form': details, 'restaurante': restau})

    else:
        form = forms.productoForm()
        return render(request, 'Platos/crearProducto.html', {'form': form, 'restaurante': restau})

def crearPla(request, rest):
    """
    Gestiona la creación de un nuevo plato para un restaurante específico.
    Muestra un formulario para añadir un plato y procesa la información enviada.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante para el cual se crea el plato.

    Returns:
        HttpResponse: Renderiza la página del formulario o redirige tras una acción exitosa.
    """

    # Obtener el restaurante por su nombre
    restau = models.restaurante.objects.filter(nombre=rest).first()

    if request.method == 'POST':
        details = forms.platoForm(request.POST)

        if details.is_valid():
            post = details.save(commit=False)
            post.restaurante = restau
            # Llamada a la función para codificar la imagen
            if 'uploadFromPC' in request.FILES:
                imagen = encode_file(request.FILES['uploadFromPC'])
                post.imagenMenu = imagen
            post.save()
            return redirect('añadirPro', rest, post.nombre)
        else:
            return render(request, "Platos/crearPlato.html", {'form': details, 'restaurante': restau})

    else:
        form = forms.platoForm()
        return render(request, 'Platos/crearPlato.html', {'form': form, 'restaurante': restau})

def editarPla(request, rest, plat):
    """
    Permite editar un plato en un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante.
        plat: Nombre del plato a editar.

    Returns:
        HttpResponse: Renderiza la página de edición del plato o redirige tras guardar los cambios.
    """
    restau = models.restaurante.objects.filter(nombre=rest).first()
    p = models.plato.objects.get(nombre=plat, restaurante=restau)

    if request.method == "POST":
        form = forms.platoForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('añadirPro', rest, p.nombre)
        else:
            # Si el formulario no es válido, renderizar de nuevo la página con el formulario y errores
            return render(request, 'Platos/editarPlato.html', {'form': form, 'restaurante': restau})
    else:
        # En caso de una solicitud GET, mostrar el formulario con la instancia del plato actual
        form = forms.platoForm(instance=p)
        return render(request, 'Platos/editarPlato.html', {'form': form, 'restaurante': restau})

def editarPro(request, rest, pro):
    """
    Permite editar un producto en un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante.
        pro: Nombre del producto a editar.

    Returns:
        HttpResponse: Renderiza la página de edición del producto o redirige tras guardar los cambios.
    """
    restau = models.restaurante.objects.filter(nombre=rest).first()
    p = models.producto.objects.get(nombre=pro, restaurante=restau)

    if request.method == "POST":
        form = forms.productoForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('productos', rest)
        else:
            # Si el formulario no es válido, renderizar de nuevo la página con el formulario y errores
            return render(request, 'Platos/editarProducto.html', {'form': form, 'restaurante': restau})
    else:
        # En caso de una solicitud GET, mostrar el formulario con la instancia del producto actual
        form = forms.productoForm(instance=p)
        return render(request, 'Platos/editarProducto.html', {'form': form, 'restaurante': restau})