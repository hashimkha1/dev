from django.urls import path

from . import views
# from .utils import convert_html_to_pdf

app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    path('data_policy/', views.data_policy, name='data_policy'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # path('team/', views.about, name='team'),
    path('team_profiles/', views.team, name='team_profiles'),
    path('client_profiles/', views.team, name='client_profiles'),
    # path('profiles/', views.profiles, name='profiles'),
    path('letter/', views.letters, name='letter'),
    path('appointment_letter/', views.letters, name='appointment_letter'),
    # path('download/', convert_html_to_pdf, name='appointment_letter_download'),

    #=======================SERVICES=====================================
    path('newservice/', views.ServiceCreateView.as_view(template_name='main/form.html'), name='newservice'),
    path('services/', views.services, name='services'),
    # path('services/<str:slug>/', views.bi_services, name='service'),
    path("display_service/<str:slug>/", views.display_service, name="display_service"),
    path("display_plans/<str:slug>/", views.service_plans, name="service_plans"),
    path('update/<int:pk>/', views.ServiceUpdateView.as_view(template_name='main/form.html'), name='update_service'),
    path('delete/<int:id>/', views.delete_service, name='delete_service'),

    #=======================SERVICES=====================================
    path('posts/', views.PostListView.as_view(), name='success'),
    path('post/new/', views.newpost, name='post-create'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<str:slug>/', views.PostDetailSlugView.as_view(), name='post-detail'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #==============DEPARTMENTS==============================================
    #==============Clint Available Time==============================================
    path('add_availability/', views.add_availability, name='add_availability'),
    path('my_availability/', views.my_availability, name='my_availability'),
    path('clints_availability/', views.clints_availability, name='clints_availability'),

    #==============DEPARTMENTS==============================================
    #---------------HUMAN RESOURCE--------------------#

    #-----------------------------FINANCE--------------------#

        #--------------------------MANAGEMENT--------------------#
        path('newprofile/', views.UserCreateView.as_view(template_name='main/form.html'), name='newprofile'),
        path('updateprofile/<int:pk>/', views.UserProfileUpdateView.as_view(template_name='main/form.html'), name='update_profile'),
        path('newplan/', views.PlanCreateView.as_view(template_name='main/form.html'), name='newplan'),
        path('plans/', views.plans, name='plans'),
        path('plan/update/<int:pk>/', views.PlanUpdateView.as_view(template_name='main/form.html'), name='update_plan'),
        path('plan/delete/<int:id>/', views.delete_plan, name='delete_plan'),
        path('meetings/', views.meetings, name='meetings'),
        path('meetings/<str:title>/', views.MeetingsUpdateView.as_view(template_name='main/form.html'), name='update_meetings'),
        
    #----------------------------IT-------------------------#
        path('it/', views.it, name='it'),
    #-----------------------finance-------------------------#
        path('finance/', views.finance, name='finance'),
        # path('marketing/', views.marketing, name='marketing'),

    path('coach_profile/', views.coach_profile, name='coach_profile'),
    path('contact/', views.contact, name='contact'),
    path('report/', views.report, name='report'),
    path('project/', views.project, name='project'),
    path('training/', views.training, name='training'),
    #path('documents/', views.codadocuments, name='documents'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('image/', views.ImageCreateView.as_view(template_name='main/form.html'), name='image'),
    path('image/<int:pk>/', views.ImageUpdateView.as_view(template_name='main/form.html'), name='updateimage'),
    path('images/', views.images, name='images'),
    path('testing/', views.testing, name='testing'),
    path('interview/', views.interview, name='interview'),

   #==============ERRORS==============================================
    path('400Error/', views.error400, name='400error'),
    path('403Error/', views.error403, name='403error'),
    path('404Error/', views.error404, name='404error'),
    path('500Error/', views.error500, name='500error'),
    # path('result/', views.result, name='result'),
    # path('noresult/', views.noresult, name='noresult'),

    path('400/', views.hendler400, name='400-error'),
    path('403/', views.hendler403, name='403-error'),
    path('404/', views.hendler404, name='404-error'),
    path('500/', views.hendler500, name='500-error'),

]