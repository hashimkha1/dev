from django.urls import path
from . import views
from .views import (TrackCreateView, TrackDeleteView, TrackDetailView,
                    TrackListView, TrackUpdateView #,UserTrackListView
                    )
                    
app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('tracker/', TrackListView.as_view(), name='tracker-list'),
    #path('user/<str:username>', UserTrackListView.as_view(), name='user-list'),
    #path('user_tracker/', UserTrackListView.as_view(), name='user-list'),
    path('usertracker', views.usertracker, name='user-list'),
    path('track/new/', TrackCreateView.as_view(), name='tracker-create'),
    path('track/<int:pk>/', TrackDetailView.as_view(), name='tracker-detail'),
    path('track/<int:pk>/update/', TrackUpdateView.as_view(), name='tracker-update'),
    path('track/<int:pk>/delete/', TrackDeleteView.as_view(), name='tracker-delete'),
    path('join/', views.join, name='join'),
    path('clients/', views.clients, name='clients'),
]  