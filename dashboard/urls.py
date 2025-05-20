from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('annuler/<str:event_id>/', views.annuler_reservation, name='annuler'),
    path('event/<event_id>/', views.event_detail_view, name='event_detail'),
    path('modifier/<str:event_id>/', views.modifier_event, name='modifier_event'),
    path('<str:event_id>/', views.reservation_event_detail, name='reservation_event_detail'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/read/<notification_id>/', views.mark_notification_read, name='mark_notification_read'),

]