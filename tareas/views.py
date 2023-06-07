from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TareasForm
from .models import Tareas
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                #guarda la sesión
                login(request, user)
                #redirecciono a la view Tareas
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Las contraseñas no coinciden'
        })

@login_required
def tareas(request):
    tareas = Tareas.objects.filter(user=request.user, datecompleted__isnull=True) # filtro de usuario y tareas sin completar
    return render(request, 'tareas.html', {'tareas': tareas})

@login_required
def tasks_completed(request):
    tareas = Tareas.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # filtro de usuario y tareas completas
    return render(request, 'tareas.html', {'tareas': tareas})

@login_required
# Creo la tarea
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html',{
            'form': TareasForm
        })
    else: #si es un metodo POST
        try:
            form = TareasForm(request.POST)
            new_tarea = form.save(commit=False)
            new_tarea.user = request.user
            new_tarea.save()
            return render(request, 'create_task.html',{
                'form': TareasForm
            })
        except ValueError:
            return render(request, 'create_task.html',{
            'form': TareasForm,
            'error': 'Los datos no son validos'
        })

@login_required
# muestro una tarea en concreto
def task_detail(request, task_id):
    if request.method == 'GET':
        tarea = get_object_or_404(Tareas, pk=task_id, user=request.user)
        form = TareasForm(instance=tarea)
        return render(request, 'task_detail.html', {'tarea': tarea, 'form': form})
    else:
        try:
            tarea = get_object_or_404(Tareas, pk=task_id, user=request.user)
            form = TareasForm(request.POST, instance=tarea)
            form.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'task_detail.html', {'tarea': tarea, 'form': form, 'error': "Error actualizando la tarea"})

@login_required
# completo la tarea
def complete_task(request, task_id):
    tarea = get_object_or_404(Tareas, pk=task_id, user=request.user)
    if request.method == 'POST':
        tarea.datecompleted = timezone.now()
        tarea.save()
        return redirect('tareas')
    
@login_required
# elimino la tarea
def delete_task(request, task_id):
    tarea = get_object_or_404(Tareas, pk=task_id, user=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')

@login_required
# Elimino la sesión
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        #si los datos que me estan enviando son validos
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña es incorrecto'
            })
        else:
            #guarda la sesión
            login(request, user)
            #redirecciono a la view Tareas
            return redirect('tareas')
