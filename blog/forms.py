from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    """
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'content',
            'img',
            'start_date',
            'end_date',
            'location',
            'is_event',
            'allow_comments',
            'publish',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'img': 'Image',
            'is_event': 'Is this an event?',
            'allow_comments': 'Allow comments?',
            'publish': 'Publish post?',
        }

class CommentForm(forms.ModelForm):
    """
    Form for users to leave a comment
    """
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }