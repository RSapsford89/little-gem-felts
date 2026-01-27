from django.db import models
from django.db.models.signals import post_save, post_delete # found in BoutiqueAdo
from django.dispatch import receiver # found in Boutique Ado
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# Create your models here.

class userProfile(models.Model):
    """
    userProfile extends the user built in model
    Extend with shipping detail, Stripe, testimonial check
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/default.jpg')
    ship_name = models.CharField(max_length=100, blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    street_address1 = models.CharField(max_length=80, blank=True, null=True)
    street_address2 = models.CharField(max_length=80, blank=True, null=True)
    town_city = models.CharField(max_length=60, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(blank_label='Country', blank=True, null=True)

    stripe_pid = models.CharField(max_length=255, blank=True, null=True)

    has_purchased = models.BooleanField(default=False) # if the user has placed an order, can leave a testimonial
    can_comment = models.BooleanField(default=False) # if the user is allowed to leave comments

    def __str__(self):
        return f'Profile for {self.user.username}'

@receiver(post_save, sender=User)
def createUpdateProfile(sender, instance, created, **kwargs):
    """
    createUpdateProfile creates or updates the userProfile
    """
    if created: # a user exists
        userProfile.objects.create(user=instance)
        instance.profile.save()

RATING = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),]


class Testimonial(models.Model):
    """
    if the user has made a purchase, allow them to leave a review
    linked to userProfile for 'has_purchased' flag. Has 'featured'
    to push it to the carousel and 'approved' to have it displayed at all
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials') # link user through the name 'testimonials'
    rating = models.IntegerField(default=5, choices=RATING)
    short_review = models.TextField(max_length=200, null=False, blank=False) # short for the carousel
    long_review = models.TextField(max_length=500, null=True, blank=True) # long for more detail if clicked on
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f'Testimonial by {self.user.username} - {self.rating}' # use WA-rating on self.rating

    def save(self, *args, **kwargs):
        """
        if testimonial rating/short/long review is edited,
        set approved to false, featured to false
        """
        if self.pk:
            try:
                testimonial = Testimonial.objects.get(pk=self.pk)
                if testimonial.rating != self.rating or testimonial.short_review != self.short_review or testimonial.long_review != self.long_review:
                    self.approved = False
                    self.featured = False

            except Testimonial.DoesNotExist:
                pass
        super().save(*args, **kwargs)
