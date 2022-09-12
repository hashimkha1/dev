from .models import ( 
                        JobRole,FeaturedCategory,
                        FeaturedSubCategory,
                        FeaturedActivity,
                        ActivityLinks
                    )

def categories (request):
    return {
        'categories': FeaturedCategory.objects.all()
    }
def subcategories (request):
    return {
        'subcategories': FeaturedSubCategory.objects.all()
    }
def activities (request):
    return {
        'activities': FeaturedActivity.objects.all()
    }
def links (request):
    return {
        'links': ActivityLinks.objects.all()
    }

def roles (request):
    return {
        'roles': JobRole.objects.all()
    }
