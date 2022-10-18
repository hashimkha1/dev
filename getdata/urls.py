from django.urls import path
from . import views
from mail.search_mail import parse_mail
from finance.utils import upload_csv
from django.urls import re_path

app_name = 'getdata'
urlpatterns = [
    path('getrating/', views.getrating, name='data-getrating'),
    path('index/', views.index, name='data-index'),
    path('upload/', views.upload_csv, name='upload'),
    path('dataupload/', views.uploaddata, name='upload-data'),
    path('datauploadcsv/', upload_csv, name='upload-data'),
    path('cashappdata/', views.CashappListView.as_view(), name='cashapp-data'),
    path('cashapp/',parse_mail, name='cashapp-email'),
#     path('gotomeeting/',views.meetingFormView,name='meetingform1'),
#     # trying a url pattern for dates
#     # gotomeetingresult
#     path('gotomeetingresult/',views.gotomeetingresult,name='gotomeetingresult'),
#     #meeting detail
#     re_path(r'^gotomeeting/(?P<meeting_id>[0-9]+)$', views.meetingView6, name='gotomeetingmeeting')


]