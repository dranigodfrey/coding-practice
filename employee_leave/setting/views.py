from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def setting(request):
    return HttpResponse('Setting Page!')