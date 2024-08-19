from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate # me sirve para no para comprobar si tiene su contrasena correcta sino que crea la cokies por nosotros
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                #para que intente guardar los datos en la base datos y si no capturar el error-- recurrir a     (except)
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # Cdo las contrasenas coiniciden usar: es para user y contrasena que se guarda: se crea el user y     password, y es guardable en la base de datos.
                user.save()
                login(request, user)
                # le dice que una vez que guarde el usuario venga a ejecutar login y le pasamos dos parametros= request y 
                return redirect('tasks')
                # con return para decirle que su trabajo acaba aca
                # sirve para redireccionar los datos del usuario a otro pagina
                #####
                #return HttpResponse('User created sucessfully')
                #Esto guarda los datos en labase de datos. y una vez que lo guarde hacer HttpResponse que     diga:Estos ultimo tres codigos son una consulta a la base de datos.y puede llegar a fallar,, y     para manejar el error usaremos> (try o excep)
            except IntegrityError:
                    return render(request, 'signup.html',{
                       'form': UserCreationForm,
                       "error": 'Username already exists'
                   })            
        return render(request, 'signup.html',{           
                # se genero el error y mandar a cliente el usuario ya existe 
            'form': UserCreationForm,
            "error": 'Password do not match'})
            # si las contrasenas no coinciden
        # Si llega a fallar algo y que estamos  mandando texto con lo dearriba, pudieramos mejorar el manejo de los errores, vamos a colocar una especie de alerta que lo pueda hacer ver mejor.
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)#me devuelve todas las tareas de la base de datos y con el filter me da solamente las tareas del usuario actualy con isnull le digo que solo me muestre esas que estan vacias o cargadas


    return render(request, 'tasks.html', {'tasks': tasks})   
 # cuando creamos usuarios es importante que nos envie a la vista de tasks: Como? 
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')#me devuelve todas las tareas de la base de datos y con el filter me da solamente las tareas del usuario actualy con isnull le digo que solo me muestre esas que estan vacias o cargadas.. el prder by es para ordenar las taeras seun ordene a la maquina
    return render(request, 'tasks.html', {'tasks': tasks})   
 # cuando creamos usuarios es importante que nos envie a la vista de tasks: Como? 

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
    }) 
    else:
        try:
            form = TaskForm(request.POST)# genera por mi un formualrio
            new_task = form.save(commit=False) # paraguardar como una instancia de la base de datos y se    pone     comit false para que no guarde y nos devuelva los datos
            new_task.user = request.user
            new_task.save()# con esto ahora generamos un dato en la base de datos
            #return render(request, 'create_task.html', {'form': TaskForm})
            return redirect('tasks')
        except ValueError:# el value error no sirve para detectar cuando tenemos un error y lo consideremos
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valida data'
        })
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)# el insta..llena el formulario con la tarea
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error updating task"})
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')




def signout(request):
    logout(request)   
    return redirect('home')

def signin(request):
    if request.method == 'GET':
         return render(request, 'signin.html',{
            'form': AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
                })
        else:
            login(request, user)
            return redirect('tasks')        
        
      