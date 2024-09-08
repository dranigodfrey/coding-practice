from django.shortcuts import render
from .forms import GenerateUsersForm
from django.contrib.auth import get_user_model

User = get_user_model()

def create_tenant(request):
    form = GenerateUsersForm()
    
    return render(request, 'tenant/create_tenant.html', {'form': form})