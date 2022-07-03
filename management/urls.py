from django.urls import path
from . import views
from .views import (
                        TaskListView,TaskDetailView,TaskCreateView,
                        TaskUpdateView,TaskDeleteView,UsertaskUpdateView,
                        TaskHistoryView,
                        UserInflowListView,AssessListView,TagCreateView,
                        InflowDetailView,#InflowCreateView,
                        InflowUpdateView,InflowDeleteView,
                        #OutflowCreateView,#OutflowListView,
                        OutflowUpdateView,OutflowDetailView,OutflowDeleteView,
                        TransactionUpdateView,TransactionListView,
                        RequirementUpdateView,RequirementDetailView,RequirementDeleteView
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


    #-----------COMPANY REPORTS---------------------------------------
    path('finance/', views.finance, name='finance'),
    path('hr/', views.hr, name='hr'),
    #path('other/', views.transact, name='management-transact'), 

    #-----------COMPANY POLICIES---------------------------------------
    path('policy/', views.policy, name='policy'),
    path('policies/', views.policies, name='policies'),
    path('benefits/', views.benefits, name='benefits'),

    #========================Employee Assessment=====================================================
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('newlink/', TaskCreateView.as_view(), name='newtask'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='taskdetail'),
    path('newevidence', views.newevidence, name='new_evidence'),
    path('evidence/',views.evidence, name='evidence'),
    path('userevidence/<str:username>/',views.userevidence, name='user_evidence'),
    path('<id>/update', views.evidence_update_view ,name='evidence_update'),
    path('taskhistory/', TaskHistoryView.as_view(), name='taskhistory'),
    path('newtask/', TaskCreateView.as_view(), name='newtask'),

    path('employee/<str:username>/',views.usertask, name='user_task'),
    path('task_employee/<int:pk>/',views.usertaskhistory, name='user_task_history'),
    path('payslip/<str:username>/',views.payslip, name='user_payslip'),
    path('task_payslip/<int:pk>/',views.task_payslip, name='task_payslip'),
    path('newtask/', TaskCreateView.as_view(), name='newtask'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='taskdetail'),
    #path('tasks/<str:username>/', UserTaskListView.as_view(), name='user-tasks'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='updatetask'),
    path('usertask/<int:pk>/update/', UsertaskUpdateView.as_view(), name='userupdatetask'),
    path('gettotalduration/', views.gettotalduration, name='gettotalduration'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='deletetask'),
    path('newcategory/', TagCreateView.as_view(), name='newcategory'),
    path('contract/',views.contract, name='contract'),

    path('assess/', views.assess, name='assess'),
    path('assessment/', AssessListView.as_view(), name='assessment'),

    path('requirement/new', views.newrequirement, name='new_requirement'),
    path('requirements/', views.requirements, name='requirements'),
    path('activerequirements/', views.active_requirements, name='requirements-active'),
    path('requirement/<int:pk>/update/', RequirementUpdateView.as_view(template_name='management/doc_templates/requirement_form.html'), name='requirement-update'),
    path('requirement/<int:pk>/delete/', RequirementDeleteView.as_view(), name='requirement-delete'),
    path('requirement/<int:pk>/', RequirementDetailView.as_view(), name='RequirementDetail'),
]
 