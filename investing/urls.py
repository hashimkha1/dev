from django.urls import path

from . import views

app_name = 'investing'
urlpatterns = [
    path('', views.home, name='home'),
    # path('covered/', views.coveredcalls, name='covered'),
    path('training/', views.training, name='training'),
    path('newinvestment/', views.newinvestment, name='newinvestment'),
    path('InvestmentPlatformOverview/', views.InvestmentPlatformOverview, name='InvestmentPlatformOverview'),
    path('newinvestmentrate/', views.newinvestmentrate, name='newinvestmentrate'),
    path('investments/', views.investments, name='investments'),
    path('companyreturns/', views.options_returns, name='companyreturns'),
    path('costbasis/', views.cost_basis, name='costbasis'),
    path('user_investments/<str:username>/', views.user_investments, name='user_investments'),
    path('options/<str:title>/', views.optiondata, name='option_list'),
    path('creditspreadupdate/<int:pk>', views.credit_spread_update, name='creditspreadupdate'),
    path('coveredupdate/<int:pk>', views.covered_update, name='coveredupdate'),
    path('shortputupdate/<int:pk>', views.shortput_update, name='shortputupdate'),
    path('overboughtsold/<str:symbol>', views.oversoldpositions, name='overboughtsold'),
    path('measures/', views.ticker_measures, name='ticker_measures'),
    path('oversoldupdate/<int:pk>', views.oversold_update.as_view(), name='oversoldupdate'),
]