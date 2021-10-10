from django.urls import path

from . import views

urlpatterns = [
    #path('', views.activity_home, name='activity_home'),
    path('', views.table, name='table'),
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
    path('task/<slug:slug>', views.task_detail, name='task_detail'),
    #path('transaction/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-updated'),

    #path('', views.index),

	#API data
	path('taskapi/', views.taskDataAPI),
	path('get_total/', views.get_total),

	#Create activity
	#path('createactivity/', views.createActivity),

	#Create activity
	path('updatetask/', views.updateTask),

	#path('deleteactivity/', views.deleteActivity),
]



