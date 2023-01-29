from django import forms
from django.utils.translation import gettext as _
from tinymce.widgets import TinyMCE
from .models import Comment, Post, Category

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField()


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        
        fields = ['title', 'subtitle', 'category_slug', 'image']
        
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        
        fields = [
            'title',
            'subtitle',
            'post_slug',
            'body',
            'category',
            'image',
            'tags',
        ]      

class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        
        fields = [
            'title',
            'subtitle',
            'image',
        ]

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        
        fields = [
            'title',
            'subtitle',
            'body',
            'category',
            'image',
        ]
        
class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label=_('Email content'))
