from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    names=["mahmud","Ahamed","jhon","abir"]
    count=0
    for name in names:
        count+=1
    context={
        "names":["mahmud","Ahamed","jhon","abir"],
        "age":23,
        "count":count
    }
    return render(request,'test.html',context)


def create_task(request):
    #employees=Employee.objects.all()
    form=TaskModelForm() #for get
    
    if request.method == "POST":
        form=TaskForm(request.POST)
        if form.is_valid():

            """"For Model Form data"""
            form.save()

            return render(request,'task_form.html',{"form":form,"message":"task added successfully"})

            ''' For Django from data'''

    context={"form": form}
    return render(request, "task_form.html", context)

def view_task(request):
    #retrive all data from task model
    tasks=Task.objects.all()

    #retrive a specific task
    task_3=Task.objects.get(pk=1)

    #fetch the 1st task
    first_task=Task.objects.first()
    return render(request,"show_task.html",{"tasks":tasks,"task3":task_3,"first_task":first_task})
    