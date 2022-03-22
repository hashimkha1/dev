from django.urls import path
from . import views
from .views import (
                    CatCreateView,CatListView,UpdateListView,CatUpdateView,CatDeleteView,
                    SubCatUpdateView,SubCatCreateView,SubCatListView,
					LinksCreateView,LinksListView,LinksUpdateView
                    )
app_name = 'testing'

urlpatterns = [
	path('', views.test_home, name='test_home'),
	path('updatelist/', UpdateListView.as_view(), name='listtoupdate'),
	path('cat/new/', CatCreateView.as_view(), name='subcat-create'),
	path('cat/<int:pk>/delete/', CatDeleteView.as_view(), name='cat-delete'),
	path('subcat/new/', SubCatCreateView.as_view(), name='subcat-create'),
	path('training/', CatListView.as_view(), name='training'),
    path('sublist/', SubCatListView.as_view(), name='subcatlist'),
	path('links/new/', LinksCreateView.as_view(), name='link-create'),
	path('links/', LinksListView.as_view(), name='links'),
	path('links/<int:pk>/update/', LinksUpdateView.as_view(), name='links-update'),

	path('cat/<int:pk>/update/', CatUpdateView.as_view(), name='update_cat'),
	path('subcat/<int:pk>/update/', SubCatUpdateView.as_view(), name='update_subcat'),
	path('training_test/', views.activity_view, name='training_test'),
	path('subtest/', views.activity_view, name='subtest'),



	
]

'''
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
	#path('tasks/<str:slug>/', TaskDetailSlugView.as_view(), name='taskdetailSlug'),
    #path('tasks/<str:user>/', TaskDetailEmployeeView.as_view(), name='usertaskdetail'),
'''
