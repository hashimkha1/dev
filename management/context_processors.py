from .models import Activity, Category, Department


def departments (request):
    return {
        'departments': Department.objects.all()
    }

def categories(request):
    return {
        #'categories': Category.objects.all()
      'categories': Category.objects.filter(level=0)
      #'categories': Category.objects.filter(level=1)
    }



def activities(request):
    return {
        'activities': Activity.objects.all()
    }