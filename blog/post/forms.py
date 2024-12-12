from django import forms
from .models import Post
from django_quill.forms import QuillFormField

class PostForm(forms.ModelForm):
    content = QuillFormField()

    class Meta:
        model = Post
        fields = ['title', 'content']