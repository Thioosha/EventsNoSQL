from django.urls import path
from . import views

urlpatterns = [
    # Mettez vos urls ici daal
    path('dashboard/', views.dashboard, name='dashboard'),
]
