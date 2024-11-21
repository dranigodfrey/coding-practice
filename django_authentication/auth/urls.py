from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    
    # class based auth generic views - routes 
    path('account/password_reset/', auth_views.PasswordResetView.as_view(template_name = 'account/password_reset.html'), name='password_reset'),
    path('account/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'account/password_reset_done.html'), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name ='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('account/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password_reset_complete.html'), name='password_reset_complete'),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(template_name = 'account/password_change.html'),  name='password_change'),
    path('account/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'account/password_change_done.html'),  name='password_change_done'),
]

    