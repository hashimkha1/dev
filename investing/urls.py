from django.urls import path

from . import views

app_name = 'investing'
urlpatterns = [
    path('', views.home, name='home'),
    path('covered/', views.coveredcalls, name='covered'),
    path('training/', views.training, name='training'),
    path('newinvestment/', views.newinvestment, name='newinvestment'),
    path('investments/', views.investments, name='investments'),
    path('user_investments/<str:username>/', views.user_investments, name='user_investments'),
    path('stockmarket/', views.OptionList.as_view(), name='stockmarket'),
    # path('options/', views.options, name='option-data'),
    path('covered_calls/', views.optiondata, name='covered_calls'),
    path('shortputdata/', views.optiondata, name='shortput'),
    path('credit_spread/', views.optiondata, name='credit_spread'),
    path('creditspreadupdate/<int:pk>', views.credit_spread_update.as_view(), name='creditspreadupdate'),
    path('coveredupdate/<int:pk>', views.covered_calls_update.as_view(), name='coveredupdate'),
    path('shortputupdate/<int:pk>', views.shortput_update, name='shortputupdate'),
    path('overboughtsold/', views.oversoldpositions, name='overboughtsold'),
    path('oversoldupdate/<int:pk>', views.oversold_update.as_view(), name='oversoldupdate'),
]