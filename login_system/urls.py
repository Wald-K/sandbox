from django.urls import path, include
from . import views

app_name = 'login_system'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
]