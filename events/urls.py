from django.urls import path
from . import views

urlpatterns = [
    # Mettez vos urls ici daal
    path('events/creer/', views.create_event, name='creer_event'),
    path('events/', views.user_events, name='user_events'),
    path('events/<str:event_id>/', views.user_event_detail, name='user_event_detail'),

    
]
