from django.shortcuts import render
from store.models import Product
from blog.models import Post

def home(request):
    """
    Docstring for home
    Updated to  also  fetch promoted products to display
    :param request: Description
    """
    promoted_products = Product.objects.filter(promoted=True).prefetch_related('images')[:3]
    blog_posts = Post.objects.filter(publish=True).order_by('-date_created')[:3]
    context = {
        'promoted_products': promoted_products,
        'blog_posts': blog_posts,
    }
    return render(request, 'home/index.html', context)
