from .models import Service,Assets
from data.models import FeaturedCategory,FeaturedSubCategory
# from .utils import image_view

#availabity of images in this app

def categories (request):
    return {
        'categories': FeaturedCategory.objects.all()
    }
    
def subcategories (request):
    return {
        'subcategories': FeaturedSubCategory.objects.all()
    }

def image_view(request):
    # images,image_names=image_view(request)
    images= Assets.objects.all()
    image_names=Assets.objects.values_list('name',flat=True)
    return {
        'images': images,
        "image_names":image_names
    }

def images(request):
    images= Assets.objects.all()
    image_names=Assets.objects.values_list('name',flat=True)
    default_url = Assets.objects.filter(name='default_emp_v1').values_list('image_url', flat=True).first()
    banner_url = Assets.objects.filter(name='banner_v1').values_list('image_url', flat=True).first()
    data_url = Assets.objects.filter(name='data_page_v1').values_list('image_url', flat=True).first()
    # print(data_url)
    return {
        'images': images,
        "image_names":image_names,
        "default_url":default_url,
        "banner_url":banner_url,
        "data_url":data_url
    }

def fetch_service_descriptions():
    # Fetch all services with a non-empty, non-null description that are active
    services_with_description = Service.objects.exclude(description__isnull=True).exclude(description='').filter(is_active=True)

    # Prepare a dictionary to hold the context data
    context_data = {}

    for service in services_with_description:
        # Use the title or slug as the key and the description as the value
        context_data[service.title] = service.description

    return context_data


def services(request):
    # services = Service.objects.all()
    services = Service.objects.filter(is_active=True)
    return {
        'main_services': services,
    }
# def googledriveurl(request):
#     return {
#         'googledriveurl':'http://drive.google.com/uc?export=view&id'
#     }

def googledriveurl(request):
    return {
        'googledriveurl': 'http://drive.google.com/uc?export=view&id='
    }
