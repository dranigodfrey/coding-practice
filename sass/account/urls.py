from django.urls import path
from . import views


urlpatterns = [
    path('user/', views.users, name='user'),
    path('create_user/', views.create_user, name='create_user'),
]