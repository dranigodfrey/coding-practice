from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts, name='accounts' ),
    path('sign_up', views.sign_up, name='sign_up' ),
    path('login', views.sign_in, name='login' ),
    path('logout', views.logout_user, name='logout' ),
]