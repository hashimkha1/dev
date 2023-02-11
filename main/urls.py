from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.layout, name='layout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.about, name='team'),
    # path('profiles/', views.profiles, name='profiles'),
    path('letter/', views.about, name='letter'),
    #==============DC48KENYA==============================================
    path('dchome', views.dclayout, name='dc_layout'),
    path('dclogin', views.dc48login, name='dc_login'),
    path('dcregister', views.register, name='dc_register'),

    #==============DEPARTMENTS==============================================
        #---------------HUMAN RESOURCE--------------------#

     #-----------------------------FINANCE--------------------#

        #--------------------------MANAGEMENT--------------------#
        path('newprofile/', views.UserCreateView.as_view(template_name='main/form.html'), name='newprofile'),
        path('update/<int:pk>/', views.UserProfileUpdateView.as_view(template_name='main/form.html'), name='update_profile'),
        path('newplan/', views.PlanCreateView.as_view(template_name='main/form.html'), name='newplan'),
        path('plans/', views.plans, name='plans'),
        path('update/<int:pk>/', views.PlanUpdateView.as_view(template_name='main/form.html'), name='update_plan'),
        path('delete/<int:id>/', views.delete_plan, name='delete_plan'),
        path('meetings/', views.meetings, name='meetings'),
        path('meetings/<str:title>/', views.MeetingsUpdateView.as_view(template_name='main/form.html'), name='update_meetings'),
        
        
        #---------------MARKETING--------------------#
        path('whatsapp/', views.runwhatsapp, name='whatsapp'),
        path('whatsapplist/', views.whatsapp_apis, name='whatsapp_list'),
        path('newwhatsapp/', views.whatsappCreateView.as_view(template_name='main/form.html'), name='whatsapp_new'),
        path('whatsapp/<int:pk>/', views.whatsappUpdateView.as_view(template_name='main/form.html'), name='whatsapp_update'),
        path('delete_whatsapp/<int:id>/', views.delete_whatsapp, name='delete_whatsapp'),


    #----------------------------IT-------------------------#
        path('it/', views.it, name='it'),
    #-----------------------finance-------------------------#
        path('finance/', views.finance, name='finance'),

    path('coach_profile/', views.coach_profile, name='coach'),
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
