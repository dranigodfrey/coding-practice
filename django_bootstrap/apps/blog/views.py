from django.shortcuts import render
from apps.blog.forms import BlogForm

# Create your views here.
def index(request):
    form = BlogForm()
    return render(request, 'blog/index.html',{'form':form})