from django.urls import path
from . import views
# from .views import WCAG_GAC_LTD_list,WCAG_CODAWCAGLTD_create,WCAG_GAC_LTD_Update,WCAG_delete,WCAG_detail
app_name = 'application'
urlpatterns = [
#     #=============================USERS VIEWS=====================================
#     # path('', views.home, name='home'),
#     path('wcaglist/',WCAG_GAC_LTD_list, name='wcaglist'),
#     path('wcagcreate/', WCAG_CODAWCAGLTD_create, name='wcagcreate'),
#     path('wcagupdate/<int:pk>/', WCAG_GAC_LTD_Update, name='wcagupdate'),
#     path('wcagdelete/<int:pk>/', WCAG_delete, name='wcagdelete'),
#     path('wcagdetail/<int:pk>/', WCAG_detail, name='wcagdetail'),
#     # path('user/<int:pk>/delete/', UserDeleteView.as_view(template_name='accounts/admin/user_delete.html'), name='user-delete'),
]