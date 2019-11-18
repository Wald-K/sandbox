from django import forms
from .models import Comment
from django_starfield import Stars

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'rating']
        widgets = {
            'rating': Stars
        }
