from django import forms
from .models import Comment, Category
from django_starfield import Stars


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'rating': Stars
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
