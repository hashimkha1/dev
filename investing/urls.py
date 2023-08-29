from django.urls import path

from . import views

app_name = 'investing'
urlpatterns = [
    path('', views.home, name='home'),
    path('covered/', views.coveredcalls, name='covered'),
    path('training/', views.training, name='training'),
    path('newinvestment/', views.newinvestment, name='newinvestment'),
    path('newinvestmentrate/', views.newinvestmentrate, name='newinvestmentrate'),
    path('investments/', views.investments, name='investments'),
    path('companyreturns/', views.options_returns, name='companyreturns'),
    path('costbasis/', views.cost_basis, name='costbasis'),
    # path('fetch_data/', views.fetch_financial_data, name='financial-data'),
    path('user_investments/<str:username>/', views.user_investments, name='user_investments'),
    path('stockmarket/', views.OptionList.as_view(), name='stockmarket'),
    path('optionlist/', views.optionlist, name='optionlist'),
    path('options/<str:title>', views.optiondata, name='option_list'),
    path('creditspreadupdate/<int:pk>', views.credit_spread_update, name='creditspreadupdate'),
    path('coveredupdate/<int:pk>', views.covered_update, name='coveredupdate'),
    path('shortputupdate/<int:pk>', views.shortput_update, name='shortputupdate'),
    path('overboughtsold/<str:symbol>', views.oversoldpositions, name='sigleoverboughtsold'),
    path('overboughtsold/', views.oversoldpositions, name='overboughtsold'),
    path('oversoldupdate/<int:pk>', views.oversold_update.as_view(), name='oversoldupdate'),
]