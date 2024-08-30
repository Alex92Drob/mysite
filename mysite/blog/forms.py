from django import forms
from .models import Post, PostImage
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'likes')
        fields = ('title', 'slug', 'body', 'status', 'tags')
        widgets = {
            'tags': TagWidget(),
        }

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ('image', )