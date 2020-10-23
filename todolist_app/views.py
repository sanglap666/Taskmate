from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist_app.models import tasklist
from todolist_app.form import taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(Response):
    
    return render(Response,'home.html')

def deletetask(Response,task_id):
    print(Response)
    task = tasklist.objects.get(pk=task_id)
    if task.manage == Response.user:
        task.delete()
        return redirect('todolist')
    else:
        return redirect('home')    

def comppend(Response,task_id):
    task = tasklist.objects.get(pk=task_id)
    if task.manage == Response.user:
        if task.done:
            task.done = False
        else:
            task.done = True
        task.save()    
        return redirect('todolist')
    else:
        return redirect('home')        

def edittask(Response,task_id):
    
    if Response.method == "POST":
        task = tasklist.objects.get(pk=task_id)
        form = taskform(Response.POST or None,instance=task)  #editing existing element
        
        if form.is_valid():
            form.save(commit=False).manage = Response.user
            form.save()
            
            messages.success(Response,"task successfully edited!")
        return redirect('todolist')
    else:
        
        task = tasklist.objects.get(pk=task_id)
        if task.manage == Response.user:
            return render(Response,'edit.html',{'task':task}) 
        else:
            return redirect('home')          

@login_required
def todolist(Response):
    
    if Response.method == "POST":
        form = taskform(Response.POST or None) #adding new element
        if form.is_valid():
            form.save(commit=False).manage = Response.user
            form.save()
            messages.success(Response,"task succesffuly added!")
        return redirect('todolist')
    else:        
        all_task = tasklist.objects.filter(manage=Response.user)
        paginator = Paginator(all_task,5)
        page = Response.GET.get('pg')
        all_task = paginator.get_page(page)
        
        return render(Response,'todolist.html',{'all_task':all_task})

def contactus(Response):
    return render(Response,'contactus.html') 

def aboutus(Response):
    return render(Response,'aboutus.html')       

