from django.contrib import admin
from .models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=(
        'title',
        'slug',
        'author',
        'content',
        'img',
        'start_date',
        'end_date',
        'location',
        'is_event',
        'allow_comments',
        'date_created',
        'date_updated',
    )


admin.site.register(Post, PostAdmin)