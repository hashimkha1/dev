from django.urls import path
from . import views
from .views import *
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
    path('cashapp/',parse_mail, name='cashapp-email'),
    path('cashappdata/', views.CashappListView.as_view(), name='cashapp-data'),
    path('cashappdetail/',views.CashappMailDetailSlugView.as_view(), name='cashappdetail'),
    path('stockmarket/', views.OptionList.as_view(), name='stockmarket'),
    path('options/', views.options, name='option-data'),
    path('covered_calls/', views.options_play_covered_calls, name='covered_calls'),
    path('shortput/', views.options_play_shortput, name='shortput'),
    path('shortputmessage/', views.options_play_shortput, name='shortput_message'),
    path('credit_spread/', views.options_play_cread_spread, name='credit_spread'),
    path('replies/',search_job_mail, name='replies-email'),
    
    path('refresh_token_goto/', refresh_token_function, name='refresh_token_function'),
    path('getmeetingresponse/', getmeetingresponse, name='getmeetingresponse'),
    path('meetingFormView/', meetingFormView, name='meetingFormView'),

    # path('gotomeeting/',views.meetingFormView,name='meetingform1'),
    # # trying a url pattern for dates
    # # gotomeetingresult
    # path('gotomeetingresult/',views.gotomeetingresult,name='gotomeetingresult'),
    # #meeting detail
    # re_path(r'^gotomeeting/(?P<meeting_id>[0-9]+)$', views.meetingView6, name='gotomeetingmeeting')
    path('testselinum/', views.selinum_test, name='testselinum'),

]