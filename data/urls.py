from django.urls import path
from . import views
from .views import (
                    FeaturedCategoryCreateView,FeaturedSubCategoryCreateView,
                    FeaturedActivityCreateView,
                    FeaturedCategoryUpdateView,FeaturedSubCategoryUpdateView,
                    FeaturedActivityUpdateView, FeaturedActivityLinksUpdateView,
                    FeaturedCategoryDeleteView,FeaturedSubCategoryDeleteView,
                    FeaturedActivityDeleteView,FeaturedActivityLinksDeleteView,
                    FeaturedCategoryListView,
                    InterviewDetailView ,InterviewUpdateView ,InterviewDeleteView,InterviewListView,
                    ClientInterviewListView,
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
    #----------------------CREATION----------------------------------------------------
    path('uploadinterview/', views.uploadinterview, name='uploadinterview'),
    #path('upload/', views.upload, name='upload'),
    #----------------------LISTING----------------------------------------------------
    path('iuploads/', InterviewListView.as_view(), name='interviewlist'),
    path('interviewuploads/', views.iuploads, name='iuploads'),
    #path('clientuploads/<str:username>', ClientInterviewListView.as_view(), name='client_uploads'),
    path('useruploads/', views.useruploads, name='user-list'),
    #path('iuploads/', UploadListView.as_view(), name='iuploads'),
    #path('uploaded/', views.uploaded, name='uploaded'),
    #----------------------DETAIL----------------------------------------------------
    path('upload/<int:pk>/',InterviewDetailView.as_view(), name='interview-detail'),
    #----------------------UPDATE----------------------------------------------------
    path('interview/<int:pk>/update', InterviewUpdateView.as_view(), name='interview-update'),
    #----------------------DELETING----------------------------------------------------
    path('interview/<int:pk>/delete', InterviewDeleteView.as_view(), name='delete-interview'),

    # TRAINING SECTION
    #----------------------Creation----------------------------------------------------
    path('category/new', FeaturedCategoryCreateView.as_view(), name='featuredcategory'),
    path('subcategory/new', FeaturedSubCategoryCreateView.as_view(), name='featuredsubcategory'),
    path('activity/new', FeaturedActivityCreateView.as_view(), name='featuredactivity'),
    #----------------------List----------------------------------------------------
    #path('list/', FeaturedCategoryListView.as_view(), name='featuredcategory-list'),
    #path('subcategory/new', FeaturedSubCategoryCreateView.as_view(), name='featuredsubcategory'),
    path('bitraining2/', views.activity_view, name='bitraining2'),  
    path('updatelist/', views.table_activity_view, name='activity-list'),
    #----------------------Update----------------------------------------------------
    path('category/<int:pk>/update', FeaturedCategoryUpdateView.as_view(), name='update-category'),
    path('subcategory/<int:pk>/update',FeaturedSubCategoryUpdateView.as_view(), name='update-subcategory'),
    path('activity/<int:pk>/update', FeaturedActivityUpdateView.as_view(), name='update-activity'),
    path('links/<int:pk>/update', FeaturedActivityLinksUpdateView.as_view(), name='update-links'),
    #----------------------Deletion----------------------------------------------------
    path('category/<int:pk>/delete', FeaturedCategoryDeleteView.as_view(), name='delete-category'),
    path('subcategory/<int:pk>/delete', FeaturedSubCategoryDeleteView.as_view(), name='delete-subcategory'),
    path('activity/<int:pk>/delete', FeaturedActivityDeleteView.as_view(), name='delete-activity'),
    path('links/<int:pk>/delete', FeaturedActivityLinksDeleteView.as_view(), name='delete-links'),



]
