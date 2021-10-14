"""DjangoEcommerce URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coda_project import settings
from testing import AdminViews, views

urlpatterns = [
    # PAGE FOR ADMIN
    path('admin_home',AdminViews.admin_home,name="admin_home"),
    
    #CATEGORIES
    path('category_list',AdminViews.CategoriesListView.as_view(),name="category_list"),
    path('category_create',AdminViews.CategoriesCreate.as_view(),name="category_create"),
    path('category_update/<slug:pk>',AdminViews.CategoriesUpdate.as_view(),name="category_update"),

    #SUBCATEGORIES

    path('sub_category_list',AdminViews.SubCategoriesListView.as_view(),name="sub_category_list"),
    path('sub_category_create',AdminViews.SubCategoriesCreate.as_view(),name="sub_category_create"),
    path('sub_category_update/<slug:pk>',AdminViews.SubCategoriesUpdate.as_view(),name="sub_category_update"),

]
