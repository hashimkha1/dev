from .models import Service
#availabity of images in this app

def images(request):
    return {
        'images': Service.objects.all()
    }

def googledriveurl(request):
    return {
        'googledriveurl':'http://drive.google.com/uc?export=view&id'
    }