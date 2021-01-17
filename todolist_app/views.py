from django.shortcuts import render,  redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator #For implementing pagination
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context = {
        'index_text':'Welcome to the Index Page'
    }
    return render(request, 'index.html', context)

@login_required
def todolist(request):
    if request.method=="POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            # form.manager = request.user
            form.save()
        messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
        
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg') #the parameter to be entered in the url
        all_tasks = paginator.get_page(page)

        return render(request, 'task.html', {'all_tasks':all_tasks})

def contact(request):
    context = {
        'contact_text':'Welcome to the Contact Page'
    }
    return render(request, 'contactus.html', context)

def about(request):
    context = {
        'about_text':'Welcome to the About page'
    }
    return render(request, 'about.html', context)

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.success(request, ("Access Denied"))
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk = task_id)
        form = TaskForm(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task Edited!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})

@login_required
def complete(request, task_id, bval):
    task = TaskList.objects.get(pk=task_id)
    #form = TaskForm(request.POST or None, instance = task) # I do not need form here...hmmmmm interesting..
    if task.manager == request.user:
        if int(bval) == 0:
            task.done = False
        else:
            task.done = True
        task.save()
        messages.success(request, ("Task Updated"))
    else:
        messages.success(request, ("Access Denied"))
    return redirect('todolist')
