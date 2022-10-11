from django.urls import path
from . import views
from mail.search_mail import parse_mail
from django.urls import re_path

app_name = 'getdata'
urlpatterns = [
    path('getrating/', views.getrating, name='data-getrating'),
    path('index/', views.index, name='data-index'),
    path('upload/', views.upload_csv, name='upload'),
    path('dataupload/', views.uploaddata, name='upload-data'),
    path('cashapp/',parse_mail, name='cashapp-data'),
#     path('gotomeeting/',views.meetingFormView,name='meetingform1'),
#     # trying a url pattern for dates
#     # gotomeetingresult
#     path('gotomeetingresult/',views.gotomeetingresult,name='gotomeetingresult'),
#     #meeting detail
#     re_path(r'^gotomeeting/(?P<meeting_id>[0-9]+)$', views.meetingView6, name='gotomeetingmeeting')


]