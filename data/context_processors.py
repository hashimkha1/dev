from .models import JobRole

def roles (request):
    return {
        'roles': JobRole.objects.all()
    }
