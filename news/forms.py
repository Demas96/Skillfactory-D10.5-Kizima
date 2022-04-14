from django.forms import ModelForm
from .models import Post, CategoryUser, Category
from django import forms



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'header', 'text', 'category']
        widgets = {
            'author': forms.HiddenInput(),
        }


class SubForm(ModelForm):
    class Meta:
        model = CategoryUser
        fields = ['user', 'category']
        widgets = {
                'user': forms.HiddenInput(),
        }



