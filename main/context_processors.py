#from .models import Service,Assets
# from data.models import FeaturedCategory,FeaturedSubCategory
# from main.models import Service,ServiceCategory,Pricing
# from .utils import image_view


#availabity of images in this app

# def categories (request):
#     return {
#         'categories': FeaturedCategory.objects.all()
#     }
    
# def subcategories (request):
#     return {
#         'subcategories': FeaturedSubCategory.objects.all()
#     }

# def image_view(request):
#     # images,image_names=image_view(request)
#     images= Assets.objects.all()
#     image_names=Assets.objects.values_list('name',flat=True)
#     return {
#         'images': images,
#         "image_names":image_names
#     }

# def images(request):
#     images= Assets.objects.all()
#     image_names=Assets.objects.values_list('name',flat=True)
#     default_url = Assets.objects.filter(name='default_emp_v1').values_list('image_url', flat=True).first()
#     banner_url = Assets.objects.filter(name='banner_v1').values_list('image_url', flat=True).first()
#     data_url = Assets.objects.filter(name='data_page_v1').values_list('image_url', flat=True).first()
    # print(data_url)
#     return {
#         'images': images,
#         "image_names":image_names,
#         "default_url":default_url,
#         "banner_url":banner_url,
#         "data_url":data_url
#     }

# def services(request):
#     services = Service.objects.all()
    # analysis_service = Service.objects.get(slug='data_analysis')
    # service_categories = ServiceCategory.objects.filter(service=analysis_service.id)
    # plans = Pricing.objects.filter(category__in=service_categories)
    # pricing_info = {
    #     obj.title: obj.price if request.user.country == 'US' else obj.discounted_price
    #     for obj in plans
    # }
    # return {
    #     'main_services': services,
        # "analysis_service": analysis_service,
        # "service_categories": service_categories,
        # "plans": plans,
        # "pricing_info": pricing_info
    #}
# def googledriveurl(request):
#     return {
#         'googledriveurl':'http://drive.google.com/uc?export=view&id'
#     }

def googledriveurl(request):
    return {
        'googledriveurl': 'http://drive.google.com/uc?export=view&id='
    }
