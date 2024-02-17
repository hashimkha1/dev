from django.urls import path
from . import views
from .views import WCAG_STANDARD_WEBSITE_List,WCAG_STANDARD_WEBSITE_create,WCAG_STANDARD_WEBSITE_Update,WCAG_STANDARD_WEBSITE_delete
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    #path('', views.home, name='home'),
    path('wcaglist/', views.WCAG_STANDARD_WEBSITE_List, name='wcaglist'),
    path('wcagcreate/', views.WCAG_STANDARD_WEBSITE_create, name='wcagcreate'),
    path('wcagupdate/<int:pk>/', views.WCAG_STANDARD_WEBSITE_Update, name='wcagupdate'),
    path('wcagdelete/<int:pk>/', views.WCAG_STANDARD_WEBSITE_delete, name='wcagdelete'),
    # path('ratingdetailview/<int:pk>', views.companyrating_detailview, name='ratingdetailview'),
    
]