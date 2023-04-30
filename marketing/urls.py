from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coda_project import settings

from . import views
from .views import (CategoriesCreate, CategoriesListView, CategoriesUpdate,
                    SubCategoriesListView)

app_name = 'marketing'
urlpatterns = [
    # PAGE FOR ADMIN
    path('',views.marketing_home,name="marketing_home"),
    
    #---------------WHATSAPP--------------------#
    path('whatsapp/', views.runwhatsapp, name='whatsapp'),
    path('whatsapplist/', views.whatsapp_apis, name='whatsapp_list'),
    path('newwhatsapp/', views.whatsappCreateView.as_view(template_name='main/form.html'), name='whatsapp_new'),
    path('whatsapp/<int:pk>/', views.whatsappUpdateView.as_view(template_name='main/form.html'), name='whatsapp_update'),
    path('delete_whatsapp/<int:id>/', views.delete_whatsapp, name='delete_whatsapp'),

]

'''
urlpatterns = [
    # PAGE FOR ADMIN
    path('',views.store_home,name="store_home"),
    
    #CATEGORIES
    path('category_list',CategoriesListView.as_view(),name="category_list"),
    path('category_create',CategoriesCreate.as_view(),name="category_create"),
    path('category_update/<slug:pk>',CategoriesUpdate.as_view(),name="category_update"),

    #SUBCATEGORIES

    path('sub_category_list',views.SubCategoriesListView.as_view(),name="sub_category_list"),
    path('sub_category_create',views.SubCategoriesCreate.as_view(),name="sub_category_create"),
    path('sub_category_update/<slug:pk>',views.SubCategoriesUpdate.as_view(),name="sub_category_update"),
    
]
'''