from .models import Service
from data.models import FeaturedCategory,FeaturedSubCategory
#availabity of images in this app

def categories (request):
    return {
        'categories': FeaturedCategory.objects.all()
    }
    
def subcategories (request):
    return {
        'subcategories': FeaturedSubCategory.objects.all()
    }

def images(request):
    return {
        'images': Service.objects.all()
    }

def googledriveurl(request):
    return {
        'googledriveurl':'http://drive.google.com/uc?export=view&id'
    }