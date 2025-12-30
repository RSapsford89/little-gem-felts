from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, blank=False,)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    main_category = models.CharField(max_length=200, blank=False)
    sub_category = models.CharField( max_length=200, blank=True, null=True)# Blank & null should be False?
    #images = models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None)# This may need to be a FK to another table which pulls in all related files...
    stock_level = models.IntegerField(default=0, blank=False, null=False)
    delivery_cost = models.DecimalField(max_digits=5, decimal_places=2)


class Images(models.Model):
    models.ImageField( upload_to=None, height_field=None, width_field=None, max_length=None)
    position = models.IntegerField(default=0, blank=True, null=True)
    primary_image = models.BooleanField(default=False)# image for card and first to display in details


class ProductID_ImageID(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    imageID = models.ForeignKey(Images, on_delete=models.CASCADE)
    date_added = models.DateTimeField( auto_now_add=True)# add the date it was added
