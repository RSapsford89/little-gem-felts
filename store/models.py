from django.db import models


# Create your models here.
class Category(models.Model):
    """
    Docstring for Category
    Category names for  use in Product as FK
    """
    name = models.CharField(max_length=50, unique=True)

    class  Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Docstring for Product
    Model containing product data. Images are contained in Image as FK
    Access images as product.images.all()
    Category is FK and on_delete is protect found on docs:
    https://docs.djangoproject.com/en/6.0/ref/models/fields/#django.db.models.ForeignKey.on_delete
    """
    name = models.CharField(max_length=200, blank=False,)
    description = models.TextField(blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    main_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    sub_category = models.CharField(max_length=200, blank=True, null=True)
    stock_level = models.IntegerField(default=0, blank=False, null=False)
    delivery_cost = models.DecimalField(max_digits=5, decimal_places=2)
    promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # suggestion by AI - needed to return the object
    # with primary_img or first image and not the string
    # so that it can be used in the basket view easily
    @property
    def primary_image(self):
        """Returns the primary image or first image if no primary is set"""
        return self.images.filter(primary_image=True).first() or self.images.first()

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', height_field=None, width_field=None, max_length=None)
    position = models.IntegerField(default=0, blank=True, null=True)
    primary_image = models.BooleanField(default=False)# image for card and first to display in details

    class Meta:
        ordering = ['position']  # Changed from 'product' to 'position'

    def __str__(self):
        return f"{self.product.name}'s image at position: {self.position}, Primary: {self.primary_image}"



