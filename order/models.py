from django.db import models
from django.db.models import Sum, Max
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import uuid
from store.models import Product
# Create your models here.

# based on Boutique Ado model
class Order(models.Model):
    """
    Model to contain order specifics
    """
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=100, blank= False, null=False)
    email = models.EmailField(blank=False, null=False)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)

    street_address1 = models.CharField(max_length=80, blank=False, null=False)
    street_address2 = models.CharField(max_length=80, blank=True, null=True)
    town_city = models.CharField(max_length=60, blank=False, null=False)
    postcode = models.CharField(max_length=20, blank=False, null=True)
    country = CountryField(blank_label='Country *', blank=False, null=False)

    date = models.DateTimeField(auto_now_add=True)
    basket= models.CharField(max_length=255)
    delivery_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    order_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    stripe_pid = models.CharField(max_length=254, blank=True, null= True)
    
    def __str__(self):
        return str(self.order_id)
    
    def update_total(self):
        """
        update the order and grand totals. Allows for editing before
        payment is confirmed by 'is_paid'
        """
        if self.is_paid is False:
            self.order_total = self.lineitems.aggregate(Sum('line_total'))['line_total__sum'] or 0
            self.delivery_cost = self.lineitems.aggregate(Max('product_delivery'))['product_delivery__max'] or 0
            self.grand_total = self.order_total + self.delivery_cost
        else:
            raise ValueError("Payment already processed, not allowed to alter the order")

# Taken from BoutiqueAdo
class OrderLineItem(models.Model):
    """
    Individul line items in a customer's order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200, null=False, blank=False)
    product_price = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    product_delivery = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    quantity = models.IntegerField(max_length=2, default=1, null=False, blank=False)
    line_total = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """
        override default save to calculate the line total
        """
        self.line_total = self.product_price * self.quantity
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.product_name}, {self.quantity} on order number: {self.order.order_id}'
