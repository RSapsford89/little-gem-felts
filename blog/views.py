from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

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
            if request.user.profile.can_comment:
                if request.method == "POST":
                    comment_form = CommentForm(request.POST)
                    try:
                        if comment_form.is_valid():
                            comment = comment_form.save(commit=False)
                            comment.post = post
                            comment.author = request.user
                            comment.save()

                            return redirect('blog:blog_details', slug=slug)
                    except Exception as e:
                        messages.error(request, f"Something went wrong at our end - please try again. {e}")
                    else:
                        messages.error(request, "Something went wrong with the for submission")
                else:
                    comment_form = CommentForm()
            else:
                messages.error(request, "Sorry you can't comment yet")
    context ={
        'post':post,
        'comments':comments,
        'comment_form':comment_form
    }
    return render(request, 'blog/blog_details.html', context)
