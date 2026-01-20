from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProfilePictureForm
from .models import userProfile
# Create your views here.

@login_required
def profile_view(request):
    """
    display the profile
    """
    return render(request, 'userprofile/profile_view.html')

@login_required
def edit_view(request):
    """
    Edit the user profile view. CustomUserFormEdit
    has no password or username field to edit.
    """
    # user = get_object_or_404(userProfile, pk=user_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile,)
        if form.is_valid():
            form.save()
            return redirect('userprofile:profile_view')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'userprofile/edit_profile.html', {'form': form, })
