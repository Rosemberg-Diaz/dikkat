from django.shortcuts import render,redirect, HttpResponse
from DataAccess import forms,models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def loginView(request):
    """
    Maneja el proceso de inicio de sesión de los usuarios.

    Args:
        request: HttpRequest que contiene los datos de la solicitud.

    Returns:
        HttpResponse: Renderiza la página de inicio de sesión o redirige tras un inicio de sesión exitoso.
    """
    if request.method == 'GET':
        return render(request, 'Usuarios/login.html', {'form': AuthenticationForm(), 'isLogin': True})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirige a una página predeterminada después del inicio de sesión
            return redirect('inicio')
        else:
            return render(request, 'Usuarios/login.html', {'form': form, 'error': "Usuario o contraseña incorrecta", 'isLogin': True})

def register(request, rest):
    """
        Maneja el registro de nuevos usuarios para un restaurante específico.

        Args:
            request: HttpRequest que contiene los datos de la solicitud.
            rest: Identificador del restaurante.

        Returns:
            HttpResponse: Renderiza la página de registro o redirige tras un registro exitoso.
        """
    if request.method == 'GET':
        return render(request, 'Usuarios/register.html',{
            'form': forms.CreateUserForm,
            'isLogin': True
        })
    else:
        if request.POST['password1'] == request.POST['password1']:
                rest = models.restaurante.objects.filter(id=request.POST['restaurante'])
                user = models.User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], rol=request.POST['rol'],email=request.POST['email'],
                                                first_name=request.POST['first_name'], last_name=request.POST['last_name'], restaurante=rest[0] )
                user.save()
                login(request, user)
                return redirect('inicio', user.restaurante)
        return render(request, 'Usuarios/register.html',{
                    'form': forms.CreateUserForm,
                    'error': 'Contraseñas no coinciden',
                     'isLogin': True
                })

def team(request, rest):
    return render(request, 'Usuarios/team.html', {'isLogin':False})

def inicio(request):
    """
       Muestra la página principal de la aplicación con una lista de todos los restaurantes.

       Args:
           request: HttpRequest que contiene los datos de la solicitud.

       Returns:
           HttpResponse: Renderiza la página principal con la lista de restaurantes.
       """
    rests = models.restaurante.objects.all()
    context={
        'restaurantes': rests,
        'tamano': range(len(rests)),
        'isLogin': True
    }
    return render(request, 'Restaurante/index.html', context)

def salir(request, rest):
    logout(request)
    return redirect("inicio", rest)
