from django.urls import path

from . import views
from .views import (PostCreateView, PostDeleteView, PostDetailView,
                    PostListView, PostUpdateView, RateCreateView, RateListView)
app_name = 'codablog'
urlpatterns = [
    path('', PostListView.as_view(), name='success'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # For Rating Purposes
    path('rate/', RateCreateView.as_view(), name='codablog-rate'),
    path('rating/', RateListView.as_view(), name='codablog-rating'),

]
