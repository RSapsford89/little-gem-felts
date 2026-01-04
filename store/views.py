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
    main_category = None
    sub_category = None
    

    context = {
        'products':products,
               }
    return render(request, 'store/products.html', context)

def product_detail(request, product_id):
    """
    Docstring for product_detail taken from BoutiqueAdo
    
    :param request: Description
    :param product_id: the product to load detail from
    """
    product = get_object_or_404(Product,pk=product_id) # Grab all the Product objects
    # The context returned to the view...
    context = {
        'product': product,
    }
    return render(request,'store/product_detail.html',  context)