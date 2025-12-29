from django.shortcuts import render
from blog.models import Post
def home(request):
    blog_posts = Post.objects.filter(publish=True).order_by('date_created')[:3]
    return render(request, 'home/index.html', {'blog_posts': blog_posts})
