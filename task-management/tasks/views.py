from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count,Max,Min
from django.contrib import messages


# Create your views here.

def manager_dashboard(request):
    

    #getting task count
    # total_task=tasks.count()
    # completed_task=Task.objects.filter(status='COMPLETED').count()
    # in_progress_task=Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task=Task.objects.filter(status='PENDING').count()
    
    # count={
    #     'total_task':
    #     'completed_task':
    #     'in_progress_task':
    #     'pending_task':
    # }

    type=request.GET.get('type','all')
    # print(type)

    counts=Task.objects.aggregate(total=Count('id')),
    completed=Count('id',filter=Q(status='COMPLETED')),
    in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
    pending=Count('id',filter=Q(status='PENDING')),

    #retriving task data

    base_query=Task.objects.select_related('details').prefetch_related('assigned_to')

    if type =='completed':
        tasks=base_query.filter(status='COMPLETED')
    elif type =='in-progress':
        tasks=base_query.filter(status='IN_PROGRESS')
    if type =='pending':
        tasks=base_query.filter(status='PENDING')
    if type =='all':
        tasks=base_query.all()
    context={
        "tasks":tasks,
        "counts":counts
    }
    return render(request, "dashboard/manager-dashboard.html",context)

# CRUD
# C=CREATE
# R=READ
# U=UPDATE
# D=DELETE


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
    task_form=TaskModelForm() #for get
    task_detail_form=TaskDetailModelForm()
    
    if request.method == "POST":
        task_form=TaskModelForm(request.POST)
        task_detail_form=TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():


            """"For Model Form data"""
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')

            ''' For Django from data'''

    context={"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)


def update_task(request,id):
    task=Task.objects.get(id=id)
    task_form=TaskModelForm(instance=task) #for get

    if task.details:
        task_detail_form=TaskDetailModelForm(instance=task.details)
    
    if request.method == "POST":
        task_form=TaskModelForm(request.POST, instance=task)
        task_detail_form=TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():


            """"For Model Form data"""
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

            ''' For Django from data'''

    context={"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)


def delete_task(request,id):
    if request.method == 'POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request,'something went wrong') 
        return redirect('manager-dashboard')


def view_task(request):
    #task_count=Task.objects.aggregate(num_task=Count('id'))
    projects=Project.objects.annotate(num_task=Count('task')).order_by('num_task') 
    return render(request,"show_task.html",{"projects":projects})
    

    #select related (ForeignKey,OneToOne Field)
    #tasks=Task.objects.select_related('task').all()
    #tasks=TaskDetail.objects.select_related('task').all()
    #tasks=Task.objects.select_related('project'.all())

    """Prefetch related(reverse ForeignKey,ManyToMany) """
    #tasks=Project.objects.prefetch_related('task_set').all()
    # tasks=Task.objects.prefetch_related('assigned_to').all()

