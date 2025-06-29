from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

def account(request):
    users  = User.objects.all()
    return render(request, 'account/account.html', {'users': users})


def health_check(request):
    return JsonResponse({"status": "ok"})