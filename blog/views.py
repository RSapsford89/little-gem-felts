from django.shortcuts import render, get_object_or_404
from .models import Post

def blog(request):
    """
    Docstring for blog
    A test view to return the blog page    
    :param request: Description
    """
    return render(request, 'blog/blog.html')

def blog_list(request):
    """
    Docstring for blog_list
    A view to return all blog articles   
    :param request: Description
    """
    posts = Post.objects.filter(publish=True).order_by('date_created')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_details(request, slug):
    """
    Docstring for blog_details
    A view to return the details of a single blog    
    :param request: Description
    """
    return render(request, 'blog/blog.html')
