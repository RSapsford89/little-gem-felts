from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ProfilePictureForm, TestimonialForm
from .models import userProfile, Testimonial
# Create your views here.

@login_required
def profile_view(request):
    """
    display the profile with testimonial form
    """
    testimonial_form = TestimonialForm()
    user_testimonial = Testimonial.objects.filter(user=request.user).first() # the first review which is retruned for this id
    if request.method == 'POST':
        # if user has bought, populate form
        if request.user.profile.has_purchased:
            testimonial_form = TestimonialForm(request.POST, instance=user_testimonial)
            # check the form is valid
            if testimonial_form.is_valid():
                testimonial = testimonial_form.save(commit=False)
                testimonial.user = request.user
                testimonial.save()
                return redirect('userprofile:profile_view')
    else:
        if user_testimonial:
            testimonial_form = TestimonialForm(instance=user_testimonial)
        else:
            testimonial_form = TestimonialForm()

    context = {
        'testimonial_form': testimonial_form,
        'user_testimonial': user_testimonial,
    }
    return render(request, 'userprofile/profile_view.html', context)

@login_required
def edit_view(request):
    """
    Edit the user profile view. CustomUserFormEdit
    has no password or username field to edit.
    """

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile,)
        if form.is_valid():
            form.save()
            return redirect('userprofile:profile_view')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'userprofile/edit_profile.html', {'form': form, })


