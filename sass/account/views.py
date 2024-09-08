from django.shortcuts import render
from django.contrib.auth import get_user_model
from account.forms import CustomUserCreationForm


User = get_user_model()

# Create your views here.
def users(request):
    users = User.objects.all()
    return render(request, 'account/users.html', {'users': users})

def create_user(request):
    form = CustomUserCreationForm
    return render(request, 'account/create_user.html', {'form': form})