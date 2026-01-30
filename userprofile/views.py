from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages
from .forms import ProfileForm, TestimonialForm
from .models import Testimonial
from order.models import Order


@login_required
def profile_view(request):
    """
    Display the profile with testimonial form and order history
    """
    # fetch testimonial if it there is one stored
    user_testimonial = Testimonial.objects.filter(user=request.user).first()
    # Get order history, sort by recent date first
    order_list = Order.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        # Check if user is allowed to review
        if request.user.profile.has_purchased:
            testimonial_form = TestimonialForm(request.POST, instance=user_testimonial)
            if testimonial_form.is_valid():
                testimonial = testimonial_form.save(commit=False)
                testimonial.user = request.user
                testimonial.save()

                # FIX: Add success message
                messages.success(request, 'Your review has been submitted!')
                return redirect('userprofile:profile_view')
            else:
                messages.error(request, 'Please correct the errors in your review.')
        else:
            messages.error(request, 'You must make a purchase before leaving a review.')
            testimonial_form = TestimonialForm()  # Reset form - should not occur, due to DTL on page

    else:
        # GET load existing review if available
        if user_testimonial:
            testimonial_form = TestimonialForm(instance=user_testimonial)
        else:
            testimonial_form = TestimonialForm()

    context = {
        'testimonial_form': testimonial_form,
        'user_testimonial': user_testimonial,
        'order_list': order_list,
    }
    return render(request, 'userprofile/profile_view.html', context)


@login_required
def edit_view(request):
    """
    Edit the user profile view.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # FIX: Add success message
            messages.success(request, 'Profile updated successfully')
            return redirect('userprofile:profile_view')
        else:
            # FIX: Add error feedback
            messages.error(request, 'Update failed. Please check the form.')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'userprofile/edit_profile.html', {'form': form})
