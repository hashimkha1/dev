from django.urls import path, include
from . import views
from .views import investStrategyList,investStrategyCreate,investStrategyUpdate,investStrategyDelete
app_name = 'application'
urlpatterns = [
# path('application/', include('application.urls')),
#=============================USERS VIEWS=====================================
#path('', views.home, name='home'),

path('strategylist/', views.investStrategyList, name='strategylist'),
path('strategycreate/', views.investStrategyCreate, name='strategycreate'),
path('strategyupdate/<int:pk>/',views.investStrategyUpdate,name='strategyupdate'),
path('strategydelete/<int:pk>/',views.investStrategyDelete,name='strategydelete'),
#path('propertydetail/<int:pk>/',views.company_properties_detail,name='propertydetail'),
]