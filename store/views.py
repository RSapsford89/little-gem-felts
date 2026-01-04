from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product

# Create your views here.
def all_products(request):
    """
    Docstring for all_products
    Retrieve all products from Product Table and filter
    if the filter input has been submitted. Show main_category
    items if buttons are pressed.
    Tutorial adapted: https://www.makeuseof.com/add-search-functionality-to-django-apps/ 
    :param request: Description
    """
    products = Product.objects.all()
    filter_query = request.GET.get("filter_input","").strip()
    category = request.GET.get("category","").strip()
    sub_category = None
    
    if category.lower() != "all":
        products = products.filter(main_category__iexact=category)

    if filter_query:
        products = products.filter(Q(name__icontains=filter_query) | Q(main_category__icontains=filter_query) | Q(description__icontains=filter_query))

    context = {
        'products':products,
        'filter_input':filter_query,
        'category':category,
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