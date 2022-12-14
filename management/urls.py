from django.urls import path
from management import views
from management.views import (
                        TaskListView,
                        TaskDetailView,TaskCreateView,
                        TaskUpdateView,TaskDeleteView,UsertaskUpdateView,
                        TaskHistoryView,
                        AssessListView,TagCreateView,TaskGroupCreateView,
                        DepartmentUpdateView,
                        RequirementUpdateView,RequirementDetailView,RequirementDeleteView
                     )

app_name = 'management'
urlpatterns = [
    path('', views.home, name='management-home'),
    #-----------COMPANY REPORTS---------------------------------------
    path('companyagenda/', views.companyagenda, name='companyagenda'),
    path('companyagenda/updatelinks', views.updatelinks_companyagenda, name='companyagenda-updatelinks'),
    path('finance/', views.finance, name='finance'),
    path('hr/', views.hr, name='hr'),
    #path('other/', views.transact, name='management-transact'),

    #-----------COMPANY POLICIES---------------------------------------
    path('policy/', views.policy, name='policy'),
    path('policies/', views.policies, name='policies'),
    path("policy/<int:pk>/update/", views.PolicyUpdateView.as_view(template_name="management/departments/hr/policy_form.html"), name="policy-update"),

    path('benefits/', views.benefits, name='benefits'),

    #========================Employee Assessment=====================================================
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('tasks/filterbycategory', views.filterbycategory, name='filterbycategory'),
    path('newlink/', TaskCreateView.as_view(), name='newlink'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='taskdetail'),
    path('newevidence/<int:taskid>', views.newevidence, name='new_evidence'),
    path('evidence/',views.evidence, name='evidence'),
    path('userevidence/<str:username>/',views.userevidence, name='user_evidence'),
    path('<id>/update', views.evidence_update_view ,name='evidence_update'),
    # path('<int:pk>/update', views.EvidenceUpdateView.as_view(template_name='management/daf/evidence_form.html') ,name='evidence_update'),
    path('taskhistory/', TaskHistoryView.as_view(), name='taskhistory'),
    path('getaveragetargets/', views.getaveragetargets, name='getaveragetargets'),
    path('employee/<str:username>/',views.usertask, name='user_task'),
    path('task_employee/<str:username>/',views.usertaskhistory, name='user_task_history'),
    # path('task_employee/<int:pk>/',views.usertaskhistory, name='user_task_history'),

    path('payslip/<str:username>/',views.pay, name='user_payslip'),
    # path('payslip/<str:username>/',views.payslip, name='user_payslip'),

    path('task_payslip/<int:pk>/',views.task_payslip, name='task_payslip'),
    # path('newtask/', TaskCreateView.as_view(), name='newtask'),
    path('newtask/', views.newtaskcreation, name='newtask'),
    path('gettasksuggestions/', views.gettasksuggestions, name='gettasksuggestions'),
    path('verifytaskgroupexists/', views.verifytaskgroupexists, name='verifytaskgroupexists'),

    #path('tasks/<str:username>/', UserTaskListView.as_view(), name='user-tasks'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='updatetask'),
    path('usertask/<int:pk>/update/', UsertaskUpdateView.as_view(), name='userupdatetask'),
    path('gettotalduration/', views.gettotalduration, name='gettotalduration'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='deletetask'),
    path('newcategory/', TagCreateView.as_view(), name='newcategory'),
    path('newtaskgroup/', TaskGroupCreateView.as_view(template_name="management/taskgroups_form.html"), name='newtaskgroup'),
    path('contract/',views.contract, name='contract'),

    path('assess/', views.assess, name='assess'),
    path('assessment/', AssessListView.as_view(), name='assessment'),
    path('session/', views.SessionCreateView.as_view(template_name="main/snippets_templates/generalform.html"), name='session'),
    path('session/<int:pk>/', views.SessionUpdateView.as_view(template_name="main/snippets_templates/generalform.html"), name='updatesession'),
    path('sessions/', views.SessionListView.as_view(), name='sessions'),
    path('user/<str:username>/',views.usersession, name='user_session'),

    path('newdepartment/', views.newdepartment, name='newdepartment'),
    path('departments/', views.department, name='departments'),
    path('department/<int:pk>/', DepartmentUpdateView.as_view(template_name='management/tag_form.html'), name='department-update'),

    path('requirement/new', views.newrequirement, name='new_requirement'),
    path('requirements/', views.requirements, name='requirements'),
    path('activerequirements/', views.active_requirements, name='requirements-active'),
    path('requirement/<int:pk>/update/', RequirementUpdateView.as_view(template_name='management/doc_templates/requirement_form.html'), name='requirement-update'),
    path('requirement/<int:pk>/delete/', RequirementDeleteView.as_view(), name='requirement-delete'),
    path('requirement/<int:pk>/', RequirementDetailView.as_view(), name='RequirementDetail'),
    path('estimate/', views.EstimateCreateView.as_view(template_name='management/activity_form.html'), name='RequirementDetail'),
    path('estimates/', views.EstimateListView.as_view(), name='estimates'),

    # path("advertisement/", views.AdsContent.as_view(), name="advertisement"),
    path("create_advertisement/", views.AdsCreateView.as_view(), name="create_advertisement"),
    path("advertisement/", views.AdsContent.as_view(), name="advertisement"),
    path("update_advertisement/<int:pk>/", views.AdsUpdateView.as_view(), name="update_advertisement"),
    path('FilterUsersByLoan/', views.FilterUsersByLoan, name='FilterUsersByLoan'),

]
