from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm

def blog_list(request):
    """
    Docstring for blog_list
    A view to return all blog articles   
    :param request: Description
    """
    posts = Post.objects.filter(publish=True).order_by('-date_created')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_details(request, slug):
    """
    Docstring for blog_details
    A view to return the details of a single blog    
    :param request: Description
    """
    post = get_object_or_404(Post, slug=slug, publish=True)
    comments = post.comments.all().order_by('-date_created')

    comment_form = None

    if post.allow_comments:
        if request.user.is_authenticated:
            if request.method == "POST":
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.post = post
                    comment.author = request.user
                    comment.save()

                    return redirect('blog:blog_details', slug=slug)
            else:
                comment_form = CommentForm()
    context ={
        'post':post,
        'comments':comments,
        'comment_form':comment_form
    }
    return render(request, 'blog/blog_details.html', context)
