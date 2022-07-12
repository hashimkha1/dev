from django.urls import path
from . import views

app_name = 'getdata'
urlpatterns = [
    path('getrating/', views.getrating, name='data-getrating'),
    path('index/', views.index, name='data-index'),
    path('gotomeeting/',views.meetingFormView,name='meetingform1'),
    # trying a url pattern for dates
    # gotomeetingresult
    path('gotomeetingresult/',views.gotomeetingresult,name='gotomeetingresult')


]