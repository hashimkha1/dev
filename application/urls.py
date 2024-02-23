from django.urls import path
from . import views
from .views import WCAG_TAB_list,WCAGTABcreate_view
app_name = 'application'
urlpatterns = [
    #=============================USERS VIEWS=====================================
#     # path('', views.home, name='home'),
path('wcaglist/',WCAG_TAB_list, name='wcaglist'),
path('wcagcreate/', WCAGTABcreate_view, name='wcagcreate'),
#     path('wcagupdate/<int:pk>/', WCAG_GAC_LTD_Update, name='wcagupdate'),
#     path('wcagdelete/<int:pk>/', WCAG_delete, name='wcagdelete'),
#     path('wcagdetail/<int:pk>/', WCAG_detail, name='wcagdetail'),
#     # path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),
 ]