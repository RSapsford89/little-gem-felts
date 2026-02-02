from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify
import uuid
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    img = ProcessedImageField(upload_to='blog_pics/', processors=[ResizeToFill(300,300)],
                              format='JPEG', options={'quality': 90}, blank=True, null=True,
                              default='profile/default-portrait.jpg')
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=200)
    is_event = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return f"{self.title}"
    
    def clean(self):
        if self.is_event:
            if self.start_date and self.end_date:
                if self.end_date <= self.start_date:
                    raise ValidationError({'end_date': "End date must be after start date."})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            if Post.objects.filter(slug=base_slug).exists():
                self.slug = f"{base_slug}-{str(uuid.uuid4())[:4]}"
            else:
                self.slug = base_slug

        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter')
    content = models.TextField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_created']

        def __str__(self):
            return f"Comment {self.content} by {self.author}"
