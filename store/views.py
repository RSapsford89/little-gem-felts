from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def all_products(request):
    """
    Docstring for all_products
    Retrieve all products from Product Table.
    :param request: Description
    """
    products = Product.objects.all()

    context = {
        'products':products,
               }
    return render(request, 'store/products.html', context)