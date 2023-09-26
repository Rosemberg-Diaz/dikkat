from django.shortcuts import render,redirect, HttpResponse
from DataAccess import forms,models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def loginView(request):
    if request.method == 'GET':
        return render(request, 'Usuarios/login.html',{
            'form': AuthenticationForm,
            'isLogin': True
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'Usuarios/login.html', {
                'form': AuthenticationForm,
                'error': "Usuario o contraseña incorrecta",
                'isLogin': True
            })
        else:
            login(request, user)
            return redirect('inicio', user.restaurante)

def register(request, rest):
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
