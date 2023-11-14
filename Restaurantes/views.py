import base64
from django.http import HttpResponse
from django.shortcuts import render, redirect
from DataAccess import forms, models
# Create your views here.
def encode_file(nombre):
    image_read = nombre.read()
    encoded_bytes = base64.b64encode(image_read)
    encoded_string = encoded_bytes.decode('utf-8')
    return (encoded_string)

def dikkat(request, rest):
    """
    Muestra información sobre un restaurante específico, incluyendo sus platos especiales.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante.

    Returns:
        HttpResponse: Renderiza la página con información sobre el restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest).first()

    if restau:
        especials = models.plato.objects.filter(restaurante=restau, especial=True)
        context = {
            'restaurante': restau,
            'especiales': especials
        }
    else:
        context = {'error': 'No se encuentra el restaurante'}

    return render(request, 'Restaurante/about.html', context)

def restauranteView(request, rest):
    """
    Muestra la página principal de un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante.

    Returns:
        HttpResponse: Renderiza la página principal del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest).first()

    if restau:
        context = {'restaurante': restau}
    else:
        context = {'error': 'No se encuentra el restaurante'}

    return render(request, 'Restaurante/index.html', context)

def menu(request, rest):
    """
    Muestra el menú de un restaurante específico, agrupando los platos por estaciones.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante.

    Returns:
        HttpResponse: Renderiza la página del menú del restaurante.
    """
    restau = models.restaurante.objects.filter(nombre=rest).first()

    if restau:
        platos = models.plato.objects.filter(restaurante=restau)

        # Generar lista de estaciones únicas
        estaciones = list({pla.estacion for pla in platos})

        context = {
            'restaurante': restau,
            'estaciones': estaciones,
            'platos': platos
        }
    else:
        context = {'error': 'No se encuentra el restaurante'}

    return render(request, 'Restaurante/menu.html', context)

def especiales(request, rest):
    """
    Muestra los platos especiales de un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante.

    Returns:
        HttpResponse: Renderiza la página con los platos especiales del restaurante o un mensaje de error.
    """
    restau = models.restaurante.objects.filter(nombre=rest).first()

    if restau:
        especials = models.plato.objects.filter(restaurante=restau, especial=True)

        # Generación de índices e ids para el front-end
        ids, idx = generar_indices(len(especials))

        context = {
            'restaurante': restau,
            'ids': ids,
            'especiales': especials,
            'tamano': idx
        }
    else:
        context = {'error': 'No se encuentra el restaurante'}

    return render(request, 'Restaurante/special-dishes.html', context)

def generar_indices(num_especiales):
    """
    Genera listas de índices e ids para los platos especiales.

    Args:
        num_especiales: Número de platos especiales.

    Returns:
        tuple: Dos listas, una de ids y otra de índices.
    """
    tipoFront = 1
    ids = []
    idx = list(range(num_especiales))

    for _ in idx:
        ids.append(tipoFront)
        tipoFront = 1 if tipoFront == 3 else tipoFront + 1

    return ids, idx

def crearRest(request):
    """
    Gestiona la creación de un nuevo restaurante.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Renderiza la página de creación del restaurante o redirige tras crear el restaurante.
    """
    if request.method == 'POST':
        form = forms.restauranteForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            # Verificar si se ha subido una imagen y codificarla
            if 'uploadFromPC' in request.FILES:
                imagen = encode_file(request.FILES['uploadFromPC'])
                post.logo = imagen

            post.save()
            return redirect('inicio', post.nombre)
        else:
            return render(request, "Restaurante/crearRestaurante.html", {'form': form, 'isLogin': True})
    else:
        form = forms.restauranteForm()
        return render(request, 'Restaurante/crearRestaurante.html', {'form': form, 'isLogin': True})

def editarRest(request, rest):
    """
    Permite editar los detalles de un restaurante específico.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.
        rest: Nombre del restaurante a editar.

    Returns:
        HttpResponse: Renderiza la página de edición del restaurante o redirige tras guardar los cambios.
    """
    p = models.restaurante.objects.get(nombre=rest)

    if request.method == "POST":
        form = forms.restauranteForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('inicio', p.nombre)
        else:
            # Si el formulario no es válido, renderizar de nuevo la página con el formulario y errores
            return render(request, 'Restaurante/editarRestaurante.html', {'form': form, 'isLogin': True})
    else:
        # En caso de una solicitud GET, mostrar el formulario con la instancia del restaurante actual
        form = forms.restauranteForm(instance=p)
        return render(request, 'Restaurante/editarRestaurante.html', {'form': form, 'isLogin': True})
