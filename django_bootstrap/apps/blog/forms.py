from django.forms import ModelForm
from apps.blog.models import Blog

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'