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

def dikkat(request,rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    especials = models.plato.objects.filter(restaurante=restau[0], especial=True)
    if len(restau) > 0:
        context = {
            'restaurante': restau[0],
            'especiales': especials
        }
    else:
        context = {
            'error': 'No se encuentra el restaurante'
        }
    return render(request, 'Restaurante/about.html',context)

def restauranteView(request, rest):
    return render(request, 'Restaurante/index.html')

def menu(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    platos = models.plato.objects.filter(restaurante=restau[0])
    estaciones = []

    for pla in platos:
        if pla.estacion not in estaciones:
            estaciones.append(pla.estacion)
    context = {
        'restaurante': restau[0],
        'estaciones': estaciones,
        'platos': platos
    }
    return render(request, 'Restaurante/menu.html', context)

def especiales(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    especials = models.plato.objects.filter(restaurante=restau[0], especial=True)
    ids = []
    idx = []
    tipoFront = 1
    cont = 0
    if len(restau) > 0:
        for i in especials:
            idx.append(cont)
            cont+=1
            ids.append(tipoFront)
            if tipoFront<=2:
                tipoFront = tipoFront + 1
            else:
                tipoFront = 1
        print(idx)
        context = {
            'restaurante': restau[0],
            'ids': ids,
            'especiales': especials,
            'tamano': idx
        }
    else:
        context = {
            'error': 'No se encuentra el restaurante'
        }
    return render(request, 'Restaurante/special-dishes.html', context)

def crearRest(request, rest):
    # check if the request is post
    if request.method == 'POST':

        # Pass the form data to the form class
        details = forms.restauranteForm(request.POST)

        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)
            imagen = encode_file(request.FILES['uploadFromPC'])
            # Finally write the changes into database
            post.save()
            p = models.restaurante.objects.get(nombre=request.POST['nombre'])
            p.logo = imagen
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('inicio', p.nombre)

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "Restaurante/crearRestaurante.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = forms.restauranteForm(None)
        return render(request, 'Restaurante/crearRestaurante.html', {'form': form})

def editarRest (request,rest):
  p = models.restaurante.objects.get(nombre=rest)
  if request.method == "POST":
     form = forms.restauranteForm(request.POST,instance=p)
     if form.is_valid():
        p.nombre = request.POST['nombre']
        p.descripcion = request.POST['descripcion']
        p.telefono = request.POST['telefono']
        p.save()
        return redirect('inicio', p.nombre)
     else :
        form = forms.restauranteForm(instance=p)
        return render(request, 'Restaurante/editarRestaurante.html', {'form': form})
  else:
    form = forms.restauranteForm(instance=p)
    return render(request, 'Restaurante/editarRestaurante.html', {'form': form})
