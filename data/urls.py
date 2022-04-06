from django.urls import path
from . import views
from .views import (
                    FeaturedCategoryCreateView,FeaturedSubCategoryCreateView,
                    FeaturedActivityCreateView,FeaturedActivityLinksCreateView,
                    FeaturedCategoryUpdateView,FeaturedSubCategoryUpdateView,
                    FeaturedActivityUpdateView, FeaturedActivityLinksUpdateView,
                    FeaturedCategoryDeleteView,FeaturedSubCategoryDeleteView,
                    FeaturedActivityDeleteView,FeaturedActivityLinksDeleteView,
                    FeaturedCategoryListView,DSUCreateView,DSUListView,
                    InterviewDetailView ,InterviewUpdateView ,
                    InterviewDeleteView,InterviewListView,InterviewCreateView,
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
    path('uploadinterview/',InterviewCreateView.as_view(template_name='data/interview/interview_form.html'), name='uploadinterview'),
    #path('upload/', views.uploadinterview, name='upload'),
    #----------------------LISTING----------------------------------------------------
    path('iuploads/', InterviewListView.as_view(), name='interviewlist'),
    path('interviewuploads/', views.iuploads, name='interviewuploads'),
    #path('clientuploads/<str:username>', ClientInterviewListView.as_view(), name='client_uploads'),
    path('useruploads/', views.useruploads, name='user-list'),
    #path('iuploads/', UploadListView.as_view(), name='iuploads'),
    #path('uploaded/', views.uploaded, name='uploaded'),
    #----------------------DETAIL----------------------------------------------------
    path('upload/<int:pk>/',InterviewDetailView.as_view(template_name='data/interview/interviews_detail.html'), name='interview-detail'),
    #----------------------UPDATE----------------------------------------------------
    path('interview/<int:pk>/update', InterviewUpdateView.as_view(template_name='data/interview/interview_form.html'), name='interview-update'),
    #----------------------DELETING----------------------------------------------------
    path('interview/<int:pk>/delete', InterviewDeleteView.as_view(template_name='data/interview/interview_confirm_delete.html'), name='delete-interview'),

    # TRAINING SECTION
    #----------------------Creation----------------------------------------------------
    path('category/new', FeaturedCategoryCreateView.as_view(template_name='data/training/form_templates/task_form.html'), name='featuredcategory'),
    path('subcategory/new', FeaturedSubCategoryCreateView.as_view(template_name='data/training/form_templates/task_form.html'), name='featuredsubcategory'),
    path('activity/new', FeaturedActivityCreateView.as_view(template_name='data/training/form_templates/task_form.html'), name='featuredactivity'),
    path('link/new', FeaturedActivityLinksCreateView.as_view(template_name='data/training/form_templates/task_form.html'), name='featuredactivity'),
    #path('dsu/new', DSUCreateView.as_view(template_name='data/training/form_templates/task_form.html'), name='dsu'),
    path('dsu/new', views.dsu_entry, name='dsu_entry'),
    #----------------------List----------------------------------------------------
    path('dsu/', DSUListView.as_view(), name='dsu'),
    #path('subcategory/new', FeaturedSubCategoryCreateView.as_view(), name='featuredsubcategory'),
    path('bitraining2/', views.activity_view, name='bitraining2'),  
    path('updatelist/', views.table_activity_view, name='activity-list'),
    #----------------------Update----------------------------------------------------
    path('category/<int:pk>/update', FeaturedCategoryUpdateView.as_view(template_name='data/training/form_templates/task_form.html'), name='update-category'),
    path('subcategory/<int:pk>/update',FeaturedSubCategoryUpdateView.as_view(template_name='data/training/form_templates/task_form.html'), name='update-subcategory'),
    path('activity/<int:pk>/update', FeaturedActivityUpdateView.as_view(template_name='data/training/form_templates/task_form.html'), name='update-activity'),
    path('links/<int:pk>/update', FeaturedActivityLinksUpdateView.as_view(template_name='data/training/form_templates/task_form.html'), name='update-links'),
    #----------------------Deletion----------------------------------------------------
    path('category/<int:pk>/delete', FeaturedCategoryDeleteView.as_view(template_name='data/training/delete_templates/task_delete.html'), name='delete-category'),
    path('subcategory/<int:pk>/delete', FeaturedSubCategoryDeleteView.as_view(template_name='data/training/delete_templates/task_delete.html'), name='delete-subcategory'),
    path('activity/<int:pk>/delete', FeaturedActivityDeleteView.as_view(template_name='data/training/delete_templates/task_delete.html'), name='delete-activity'),
    path('links/<int:pk>/delete', FeaturedActivityLinksDeleteView.as_view(template_name='data/training/delete_templates/task_delete.html'), name='delete-links'),



]
