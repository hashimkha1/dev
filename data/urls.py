from django.urls import path
from . import views
from .views import (
                    FeaturedCategoryCreateView,FeaturedSubCategoryCreateView,FeaturedActivityCreateView,
                    InterviewDetailView ,InterviewUpdateView ,InterviewDeleteView
                    #TrackCreateView, TrackDeleteView, TrackDetailView,
                    #TrackListView, InterviewUpdateView #,UserTrackListView
                    )


app_name = 'data'
urlpatterns = [
    path('', views.analysis, name='home'),
    path('report/', views.report, name='report'),
    path('etl/', views.etl, name='etl'),
    path('database/', views.database, name='database'),
    path('financialsystem/', views.financialsystem, name='finance'),
    path('payroll/', views.payroll, name='payroll'),
    path('project/', views.project, name='project'),
    path('training/', views.training, name='training'),
    path('training_v2/', views.training_v2, name='training_v2'),
    path('bitraining/', views.bitraining, name='bitraining'),
    path('bitraining2/', views.activity_view, name='bitraining2'),
    path('interview/', views.interview, name='interview'),

    path('deliverable/', views.deliverable, name='deliverable'),
    path('getdata/', views.getdata, name='getdata'),
    path('pay/', views.pay, name='pay'),

    #Interview/Assignment Section
    path('uploadinterview/', views.uploadinterview, name='uploadinterview'),
    path('iuploads/', views.iuploads, name='iuploads'),
    path('useruploads/', views.useruploads, name='user-list'),
    path('upload/<int:pk>/',InterviewDetailView.as_view(), name='interview-detail'),
    path('interview/<int:pk>/update', InterviewUpdateView.as_view(), name='interview-update'),
    path('interview/<int:pk>/delete', InterviewDeleteView.as_view(), name='delete-interview'),
    #path('iuploads/', UploadListView.as_view(), name='iuploads'),
    #path('upload/', views.upload, name='upload'),
    #path('uploaded/', views.uploaded, name='uploaded'),


    # TRAINING SECTION
    #----------------------Creation----------------------------------------------------
    path('category/new', FeaturedCategoryCreateView.as_view(), name='featuredcategory'),
    path('subcategory/new', FeaturedSubCategoryCreateView.as_view(), name='featuredsubcategory'),
    path('activity/new', FeaturedActivityCreateView.as_view(), name='featuredactivity'),
    #----------------------List----------------------------------------------------
    #path('category/new', FeaturedCategoryCreateView.as_view(), name='featuredcategory'),
    #path('subcategory/new', FeaturedSubCategoryCreateView.as_view(), name='featuredsubcategory'),
    #----------------------Update----------------------------------------------------

    #----------------------Deletion----------------------------------------------------

    path('bitraining2/', views.activity_view, name='bitraining2'),
    path('iuploads/', views.iuploads, name='iuploads'),
    path('useruploads/', views.useruploads, name='user-list'),
    path('upload/<int:pk>/',InterviewDetailView.as_view(), name='interview-detail'),
    path('interview/<int:pk>/update', InterviewUpdateView.as_view(), name='interview-update'),
    path('interview/<int:pk>/delete', InterviewDeleteView.as_view(), name='delete-interview'),
    #path('iuploads/', UploadListView.as_view(), name='iuploads'),
    #path('upload/', views.upload, name='upload'),
    #path('uploaded/', views.uploaded, name='uploaded'),



]
