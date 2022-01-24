from django.urls import path
from . import views
from .views import (
                        
                        UserInflowListView,#InflowListView,
                        InflowDetailView,#InflowCreateView,
                        InflowUpdateView,InflowDeleteView,
                        #OutflowCreateView,#OutflowListView,
                        OutflowUpdateView,OutflowDetailView,OutflowDeleteView,
                        TransactionUpdateView,TransactionListView 
                     )

app_name = 'management'
urlpatterns = [
    path('', views.home, name='management-home'),
    path('transact/', views.transact, name='management-transact'),
    #path('transaction/', views.transaction, name='management-transaction'),
    path('transaction/', TransactionListView.as_view(), name='transaction-list'),
    #path('transaction/', OutflowDetailView.as_view(), name='transaction-detail'),
    path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-update'),

    #-----------CASHINFLOW---------------------------------------
    path('inflow_entry/', views.inflow, name='entry_inflow'),
    #path('inflow/', InflowListView.as_view(), name='inflow-list'),
    path('inflows/', views.inflows, name='inflow-list'),
    path('user_inflow/', UserInflowListView.as_view(), name='user-list'),
    #path('inflow/new/', InflowCreateView.as_view(), name='inflow-create'),
    path('inflow/<int:pk>/', InflowDetailView.as_view(), name='inflow-detail'),
    path('inflow/<int:pk>/update/', InflowUpdateView.as_view(), name='inflow-update'),
    path('inflow/<int:pk>/delete/', InflowDeleteView.as_view(), name='inflow-delete'),

    #-----------CASHOUTFLOW---------------------------------------
    path('outflow_entry/', views.outflow_entry, name='outflow_entry'),
    #path('outflow/', OutflowListView.as_view(), name='outflow-list'),
    path('outflows/', views.outflowlist, name='outflow-list'),
    #path('outflow/new/', OutflowCreateView.as_view(), name='outflow-create'),
    #path('user_outflow/', UseroutflowListView.as_view(), name='user-list'),
    path('outflow/<int:pk>/', OutflowDetailView.as_view(), name='outflow-detail'),
    path('outflow/<int:pk>/update/', OutflowUpdateView.as_view(), name='outflow-update'),
    path('outflow/<int:pk>/delete/', OutflowDeleteView.as_view(), name='outflow-delete'),   

]
 