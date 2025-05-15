from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('inscription1/', views.account_type_view, name='account_type'),
    path('inscription2/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('settings/', views.user_settings_view, name='settings'),

]
