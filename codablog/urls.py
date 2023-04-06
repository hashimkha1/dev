from django.urls import path

from . import views
from .views import ( #PostCreateView, 
                    PostDeleteView, PostDetailView,
                    PostListView, PostUpdateView)
app_name = 'codablog'
urlpatterns = [
    path('', PostListView.as_view(), name='success'),
    path('post/new/', views.newpost, name='post-create'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
