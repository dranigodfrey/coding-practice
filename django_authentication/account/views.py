from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView
)
from account.forms import(
    CustomUserCreationForm,
    GroupForm,
    AddUsersToGroupForm,
    UserGroupForm,
)
from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView,
    LogoutView
)
from django.contrib.auth.models import(
    Group,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404


User = get_user_model()

class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'account/user_list.html'


class UserDetailView(DetailView):
    model = User
    template_name = 'account/user_detail.html'


class SignUpView(CreateView):
    model  = User
    form_class = CustomUserCreationForm
    template_name = 'account/sign_up.html'
    success_url = reverse_lazy('user-list')


class SignInView(LoginView):
    redirect_authenticated_user = True
    template_name = 'account/sign_in.html'

    def get_success_url(self):
        return reverse_lazy('user-list') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

class SignOutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('sign-in')


class UserDeleteView(DeleteView):
    model = User
    template_name = 'account/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')


class UserUpdateView(UpdateView):
    model = User
    fields = ('username', 'email', 'user_role')
    template_name = 'account/user_update.html'
    success_url = reverse_lazy('user-list')


class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'account/group_list.html'


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'account/group_create.html'
    success_url = reverse_lazy('group-list')


class GroupDetialView(DetailView):
    model = Group
    template_name = 'account/group_detail.html'


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'account/group_update.html'
    success_url = reverse_lazy('group-list')


class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'account/group_confirm_delete.html'
    success_url = reverse_lazy('group-list')

 
class AddUsersToGroupView(FormView):
    template_name = 'account/add_users_to_group.html'
    form_class = AddUsersToGroupForm
    success_url = reverse_lazy('group-list')

    def get_initial(self):
        initial = super().get_initial()
        group_id = self.kwargs.get('group_id')
        if group_id:
            group = get_object_or_404(Group, id=group_id)
            initial['group'] = group
            initial['users'] = group.user_set.all()
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        group_id = self.kwargs.get('group_id')
        if group_id:
            group = get_object_or_404(Group, id=group_id)
            kwargs['initial'] = {'group': group, 'users': group.user_set.all()}
        return kwargs

    def form_valid(self, form):
        group = form.cleaned_data['group']
        users = form.cleaned_data['users']
        group.user_set.set(users)  # Update the users in the group
        return super().form_valid(form)
    

class UserGroupView(FormView):
    template_name = 'account/user_group.html'
    form_class = UserGroupForm
    success_url = reverse_lazy('user-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.kwargs.get('user_id')
        if user_id:
            kwargs['user'] = User.objects.get(pk=user_id)
        return kwargs

    def form_valid(self, form):
        user = form.cleaned_data['user']
        groups = form.cleaned_data['groups']
        user.groups.set(groups)
        return super().form_valid(form)
    

class GroupMembershipView(ListView):
    model = User
    template_name = 'account/group_membership.html'
    context_object_name = 'users'
