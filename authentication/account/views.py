from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
@login_required
def accounts(request):
    users = User.objects.all()
    context = {
        'users':users
    }
    return render(request, template_name='account/index.html', context=context)

def sign_up(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, template_name='account/sign_up.html', context=context)

def sign_in(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('accounts')
        else:
            return HttpResponse('Login denied!')
    return render(request, template_name='account/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')