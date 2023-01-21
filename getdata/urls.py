from django.urls import path
from . import views
from mail.search_mail import parse_mail, search_job_mail
from finance.utils import upload_csv
from django.urls import re_path
from gapi.gservices import cashapp_main
from getdata.utils import main_cread_spread
app_name = 'getdata'
urlpatterns = [
    path('getrating/', views.getrating, name='data-getrating'),
    path('index/', views.index, name='data-index'),
    path('upload/', views.upload_csv, name='upload'),
    path('dataupload/', views.uploaddata, name='upload-data'),
    path('bigdata/', views.bigdata, name='generate-data'),
    path('datauploadcsv/', upload_csv, name='upload-data'),
    path('cashappdata/', views.CashappListView.as_view(), name='cashapp-data'),
    path('stockmarket/', views.OptionList.as_view(), name='stockmarket'),
    path('options/', views.options, name='option-data'),

    path('covered_calls/', views.refresh_token_function, name='covered_calls'),
    path('shortput/', views.meetingFormView, name='shortput'),
    path('credit_spread/', main_cread_spread, name='credit_spread'),

    path('cashapp/',parse_mail, name='cashapp-email'),
    path('replies/',search_job_mail, name='replies-email'),
    
    path('gotomeeting/',views.refresh_token_function,name='gotomeeting'),
    # trying a url pattern for dates
    # gotomeetingresult
    path('gotomeetingresult/',views.meetingView6,name='gotomeetingresult'),
    #meeting detail
    re_path(r'^gotomeeting/(?P<meeting_id>[0-9]+)$', views.meetingView6, name='gotomeetingmeeting')

]