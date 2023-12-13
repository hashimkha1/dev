from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coda_project import settings

from . import views
# from .views import (CategoriesCreate, CategoriesListView, CategoriesUpdate,
#                     SubCategoriesListView)

app_name = 'marketing'
urlpatterns = [
    # PAGE FOR ADMIN
    path('',views.marketing,name="marketing"),
    
    
    #---------------WHATSAPP--------------------#
    path('email_ads/', views.send_email_ads, name='email_ads'),
    path('whatsapp/', views.runwhatsapp, name='whatsapp'),
    path('whatsapplist/', views.whatsapp_apis, name='whatsapp_list'),
    path('newwhatsapp/', views.whatsappCreateView.as_view(template_name='main/form.html'), name='whatsapp_new'),
    path('whatsapp/<int:pk>/', views.whatsappUpdateView.as_view(template_name='main/form.html'), name='whatsapp_update'),
    path('delete_whatsapp/<int:id>/', views.delete_whatsapp, name='delete_whatsapp'),
    path('adslist/', views.ads, name='ads_list'),
    path('newad/', views.AdsCreateView.as_view(template_name='main/form.html'), name='ads_new'),
    path('ad/<int:pk>/', views.AdsUpdateView.as_view(template_name='main/form.html'), name='ad_update'),
    path('delete_ad/<int:id>/', views.delete_ads, name='delete_ad'),
    # path('whatsapp_status/', views.whatsapp_status, name='whatsapp_status'),

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