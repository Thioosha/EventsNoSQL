from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('event/<event_id>/', views.event_detail_view, name='event_detail'),
]