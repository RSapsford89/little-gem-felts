from django import forms
from django.utils import timezone
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    """
    class Meta:
        model = Post
        fields = [
            'title',
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

    def clean(self):
        cleaned_data = super().clean()
        is_event = cleaned_data.get('is_event')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        # check for EVENT flag first
        if is_event:
            now = timezone.now()

            # Check if start date is in the past
            if start_date and start_date < now:
                self.add_error('start_date', "The event cannot start in the past.")

            # Check if end date is before start date
            if start_date and end_date and end_date <= start_date:
                self.add_error('end_date', "The end date must be after the start date.")

        return cleaned_data


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
