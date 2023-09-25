from django.shortcuts import render, redirect
from DataAccess import forms, models
import base64

def encode_file(nombre):
    image_read = nombre.read()
    encoded_bytes = base64.b64encode(image_read)
    encoded_string = encoded_bytes.decode('utf-8')
    return (encoded_string)

def products(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    productos = models.producto.objects.filter(restaurante=restau[0])

    context = {
        'restaurante': restau[0],
        'productos': productos,
    }
    return render(request, 'Platos/productos.html', context)


def proByPla(request, rest, pla):
    restau = models.restaurante.objects.filter(nombre=rest)
    products = models.producto.objects.filter(restaurante=restau[0])
    plat = models.plato.objects.filter(nombre=pla)
    inv = models.inventario.objects.filter(restaurante=restau[0], plato=plat[0])
    if len(products) == 0:
        products = 0
    if request.method == 'POST':
        # Pass the form data to the form class
        details = forms.productPlatoForm(request.POST)

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
            prod = models.producto.objects.filter(restaurante=restau[0], nombre=request.POST['producto'])
            p = models.inventario.objects.get(producto=None, restaurante=None, plato=None, cantidadGastada=request.POST['cantidadGastada'])
            p.producto = prod[0]
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
    restau = models.restaurante.objects.filter(nombre=rest)
    # check if the request is post
    if request.method == 'POST':
        # Pass the form data to the form class
        details = forms.productoForm(request.POST, request.FILES)

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
            p = models.producto.objects.get(nombre=request.POST['nombre'])
            p.restaurante = models.restaurante.objects.get(nombre=rest)
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('productos', rest)

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "Platos/crearProducto.html", {'form': details,  'restaurante': restau[0]})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = forms.productoForm(None)
        return render(request, 'Platos/crearProducto.html', {'form': form,  'restaurante': restau[0]})

def crearPla(request, rest):
    restau = models.restaurante.objects.filter(nombre=rest)
    context = {
        'restaurante': restau[0],
    }
    # check if the request is post
    if request.method == 'POST':

        # Pass the form data to the form class
        details = forms.platoForm(request.POST)

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
            imagen = encode_file(request.FILES['uploadFromPC'])
            p = models.plato.objects.get(nombre=request.POST['nombre'])
            p.restaurante = models.restaurante.objects.get(nombre=rest)
            p.imagenMenu = imagen
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('añadirPro', rest, p.nombre)

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "Platos/crearPlato.html", {'form': details,  'restaurante': restau[0]})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = forms.platoForm(None)
        return render(request, 'Platos/crearPlato.html', {'form': form,  'restaurante': restau[0]})

def editarPla (request,rest, plat):
  restau = models.restaurante.objects.filter(nombre=rest)
  p = models.plato.objects.get(nombre=plat)
  if request.method == "POST":
     form = forms.platoForm(request.POST,instance=p)
     if form.is_valid():
        p.nombre = request.POST['nombre']
        p.descripcion = request.POST['descripcion']
        p.estacion = request.POST['estacion']
        p.precio = request.POST['precio']
        p.restaurante = models.restaurante.objects.get(nombre=rest)
        p.save()
        return redirect('añadirPro', rest, p.nombre)
     else :
        form = forms.platoForm(instance=p)
        return render(request, 'Platos/editarPlato.html', {'form': form,  'restaurante': restau[0]})
  else:
    form = forms.platoForm(instance=p)
    return render(request, 'Platos/editarPlato.html', {'form': form,  'restaurante': restau[0]})

def editarPro (request,rest, pro):
  restau = models.restaurante.objects.filter(nombre=rest)
  p = models.producto.objects.get(nombre=pro)
  if request.method == "POST":
     form = models.productoForm(request.POST,instance=p)
     if form.is_valid():
        p.nombre = request.POST['nombre']
        p.unidadMedida = request.POST['unidadMedida']
        p.precio = request.POST['precio']
        p.estado = request.POST['estado']
        p.cantidadDisponible = request.POST['cantidadDisponible']
        p.restaurante = models.restaurante.objects.get(nombre=rest)
        p.save()
        return redirect('productos', rest)
     else :
        form = forms.productoForm(instance=p)
        return render(request, 'Platos/editarProducto.html', {'form': form,  'restaurante': restau[0]})
  else:
    form = forms.productoForm(instance=p)
    return render(request, 'Platos/editarProducto.html', {'form': form,  'restaurante': restau[0]})