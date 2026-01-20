from django.contrib import admin
from .models import userProfile, Testimonial
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ship_name',
        'phoneNumber',
        'street_address1',
        'street_address2',
        'town_city',
        'postcode',
        'country',
        'has_purchased',
        'can_comment',
    ]

class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    list_display = [
        'user',
        'rating',
        'approved',
        'short_review',
        'featured',
        'date_created',
    ]
    fields = [
        'user',
        'rating',
        'approved',
        'short_review',
        'long_review',
        'featured',
    ]
    readonly_fields = ['date_created','date_edited']


admin.site.register(userProfile, UserProfileAdmin)
admin.site.register(Testimonial, TestimonialAdmin)