
'''
import random
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Task, Category,Activity
from django.http import JsonResponse
'''
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

'''
def get_total(request):
    title = 'All Tasks'
    queryset = Task.objects.all()
    total_earning = Task.objects.aggregate(Sum("mx_earning"))
    context = {
    "title": title,
    "queryset": queryset,
    "total_earning": total_earning,
    }
    return render(request, 'testing/table.html', context)


#API data
def taskDataAPI(request):
    data = Task.objects.all()
    dataList = []
    for i in data:
        dataList.append({
                            'name':i.task_name,
                            'submission':i.updated,
                            'deadline':i.deadline,
                            'late_penalty':i.late_penalty,
                            'point':i.point,
                            'mxpoint':i.mx_point,
                            'earning':i.mx_earning,
                            'pay':i.pay,
                            'id':i.id
                         })
    
    return JsonResponse(dataList, safe=False)

''' 
@csrf_exempt
def createActivity(request):
    name = request.POST.get('name')
    point = request.POST.get('point') 
    mxpoint = request.POST.get('mxpoint')
    earning = request.POST.get('earning')
    

    Activity.objects.create(
		name=name,
        point=point,
        mxpoint=mxpoint,
        earning=earning,
		)
    return JsonResponse('Activity Created!', safe=False)
'''
@csrf_exempt
def updateTask(request):
    objId = request.POST.get('id')
    point = request.POST.get('point')

    task = Task.objects.get(id=objId)
    task.point = point
    task.save()

    return JsonResponse('task Updated!', safe=False)

@csrf_exempt
def deleteTask(request):
	print('Delete called!')
	objId = request.POST.get('id')
	task = Task.objects.get(id=objId)
	task.delete()

	return JsonResponse('Task Deleted!', safe=False)



def task_home(request):
    return render(request, 'main/layout.html', {'title': 'task'})

def table(request):
    #activities =Activity.activities.all()
    tasks=Task.objects.all()
    context = {
        'tasks': tasks,
    }
    return render(request, 'testing/table.html',context)

def task_detail(request, category_slug, slug):
    task = get_object_or_404(Task, slug=slug)
    #task.num_visits = task.num_visits + 1
    #task.last_visit = datetime.now()
    task.save()

    related_tasks = list(task.category.tasks.filter(parent=None).exclude(id=task.id))
    
    if len(related_tasks) >= 3:
        related_tasks = random.sample(related_tasks, 3)

    if task.parent:
        return redirect('task_detail', category_slug=category_slug, slug=task.parent.slug)

    context = {
        'task': task,
        'related_tasks': related_tasks
    }
    return render(request, 'testing/table.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tasks = category.task.filter(parent=None)

    context = {
        'category': category,
        'tasks': tasks
    }
    return render(request, 'testing/category_detail.html', context)

'''
