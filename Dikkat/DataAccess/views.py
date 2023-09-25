from django.shortcuts import render,redirect, HttpResponse
from .models import plato
from .forms import CreateUserForm, restauranteForm, platoForm, productoForm, productPlatoForm

from .models import User, restaurante, plato, producto, inventario


def products(request, rest):
    restau = restaurante.objects.filter(nombre=rest)
    productos = producto.objects.filter(restaurante=restau[0])

    context = {
        'restaurante': restau[0],
        'productos': productos,
    }
    return render(request, 'productos.html', context)


def proByPla(request, rest, pla):
    restau = restaurante.objects.filter(nombre=rest)
    plat = plato.objects.filter(nombre=pla)
    inv = inventario.objects.filter(restaurante=restau[0], plato=plat[0])

    if request.method == 'POST':
        # Pass the form data to the form class
        details = productPlatoForm(request.POST)

        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)
            # Finally write the changes into database
            post.save()
            p = inventario.objects.get(producto=request.POST['producto'], restaurante=None, plato=None)
            p.restaurante = restau[0]
            p.plato = plat[0]
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('añadirPro', rest, pla)

        else:
            if len(inv) > 0:
                context = {
                    'restaurante': restau[0],
                    'plato': plat[0],
                    'inventario': inv,
                    'form': details
                }
            else:
                context = {
                    'restaurante': restau[0],
                    'plato': plat[0],
                    'error': 'No se encontraron producto asociados',
                    'form': details
                }
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "productosByPlatos.html", context)
    else:
        form = productPlatoForm(None)
        if len(inv) > 0:
            context = {
                'restaurante': restau[0],
                'plato': plat[0],
                'inventario': inv,
                'form': form
            }
        else:
            context = {
                'restaurante': restau[0],
                'plato': plat[0],
                'error': 'No se encontraron producto asociados',
                'form': form
            }
        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page

        return render(request, 'productosByPlatos.html', context)

def crearPro(request, rest):
    # check if the request is post
    if request.method == 'POST':
        # Pass the form data to the form class
        details = productoForm(request.POST)

        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)
            # Finally write the changes into database
            post.save()
            p = producto.objects.get(nombre=request.POST['nombre'])
            p.restaurante = restaurante.objects.get(nombre=rest)
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return HttpResponse("data submitted successfully")

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "crearProducto.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = productoForm(None)
        return render(request, 'crearProducto.html', {'form': form})

def crearPla(request, rest):
    # check if the request is post
    if request.method == 'POST':

        # Pass the form data to the form class
        details = platoForm(request.POST)

        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():

            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)

            # Finally write the changes into database
            post.save()
            p = plato.objects.get(nombre=request.POST['nombre'])
            p.restaurante = restaurante.objects.get(nombre=rest)
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('añadirPro', rest, p.nombre)

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "crearPlato.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = platoForm(None)
        return render(request, 'crearPlato.html', {'form': form})

def editarPla (request,rest, plat):
  p = plato.objects.get(nombre=plat)
  if request.method == "POST":
     form = platoForm(request.POST,instance=p)
     if form.is_valid():
        p.nombre = request.POST['nombre']
        p.descripcion = request.POST['descripcion']
        p.estacion = request.POST['estacion']
        p.precio = request.POST['precio']
        p.restaurante = restaurante.objects.get(nombre=rest)
        p.save()
        return redirect('añadirPro', rest, p.nombre)
     else :
        form = platoForm(instance=p)
        return render(request, 'editarPlato.html', {'form': form})
  else:
    form = platoForm(instance=p)
    return render(request, 'editarPlato.html', {'form': form})

def editarPro (request,rest, pro):
  p = producto.objects.get(nombre=pro)
  if request.method == "POST":
     form = productoForm(request.POST,instance=p)
     if form.is_valid():
        p.nombre = request.POST['nombre']
        p.unidadMedida = request.POST['unidadMedida']
        p.precio = request.POST['precio']
        p.estado = request.POST['estado']
        p.cantidadDisponible = request.POST['cantidadDisponible']
        p.restaurante = restaurante.objects.get(nombre=rest)
        p.save()
        return redirect('productos', rest)
     else :
        form = productoForm(instance=p)
        return render(request, 'editarProducto.html', {'form': form})
  else:
    form = productoForm(instance=p)
    return render(request, 'editarProducto.html', {'form': form})

