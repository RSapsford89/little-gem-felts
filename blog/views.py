from django.shortcuts import render


def blog(request):
    """
    Docstring for blog
    A test view to return the blog page    
    :param request: Description
    """
    return render(request, 'blog/blog.html')

def blog_list(request):
    """
    Docstring for blog
    A view to return the blog page    
    :param request: Description
    """
    return render(request, 'blog/blog.html')
