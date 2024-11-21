from django.urls import path
from account.views import (
    SignUpView,
    UserListView,
    UserDetailView,
    SignInView,
    SignOutView,
    UserDeleteView,
    UserUpdateView,
    GroupCreateView,
    GroupListView,
    GroupUpdateView,
    GroupDetialView,
    GroupMembershipView,
    GroupDeleteView,
    AddUsersToGroupView,
    UserGroupView,
)

urlpatterns = [
    path('sign-up/', SignUpView.as_view() , name='sign-up'),
    path('sign-in/', SignInView.as_view() , name='sign-in'),
    path('sign-out/', SignOutView.as_view(
        http_method_names = ['get', 'post', 'options']),
        name='sign-out'
    ),
    path('user-list/', UserListView.as_view() , name='user-list'),
    path('delete-user/<int:pk>',UserDeleteView.as_view() , name='delete-user'),
    path('user-detail/<int:pk>', UserDetailView.as_view() , name='user-detail'),
    path('update-user/<int:pk>', UserUpdateView.as_view() , name='update-user'),

    # groups and permission routes 
    path('group/', GroupCreateView.as_view(), name='group'),
    path('group-list/', GroupListView.as_view(), name='group-list'),
    path('group-detail/<int:pk>', GroupDetialView.as_view(), name='group-detail'),
    path('group-update/<int:pk>', GroupUpdateView.as_view(), name='group-update'),
    path('group-delete/<int:pk>', GroupDeleteView.as_view(), name='group-delete'),
    path('group-membership/', GroupMembershipView.as_view(), name='group-membership'),
    path('add_users_to_group/<int:group_id>/', AddUsersToGroupView.as_view(), name='add_users_to_group'),
    path('user_group/<int:user_id>/', UserGroupView.as_view(), name='user_group'),
   ]