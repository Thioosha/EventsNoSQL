from django.urls import path
from . import views

urlpatterns = [
    path('creer/<str:event_id>/', views.create_reservation, name='creer_reservation'),
    path('confirm/<str:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('validated/', views.validated_reservation, name='validated_reservation'),
]
