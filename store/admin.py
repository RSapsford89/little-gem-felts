from django.contrib import admin
from .models import Product, Images
# Register your models here.


class ImagesInline(admin.StackedInline):
    model = Images
    extra =  8
    fields = ['image', 'position', 'primary_image']


class ProductAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'description',
        'price',
        'main_category',
        'sub_category',
        'stock_level',
        'delivery_cost',
    )
    inlines = [ImagesInline]


admin.site.register(Product, ProductAdmin)