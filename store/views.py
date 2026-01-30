from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
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
    promoted_products = Product.objects.filter(promoted=True).prefetch_related('images')[:3]
    filter_query = request.GET.get("filter_input", "").strip()
    category = request.GET.get("category", "").strip()
    sub_category = None # for later development
    products = Product.objects.filter(stock_level__gt=0)

    if category and category.lower() != "all":
        products = products.filter(main_category__name__icontains=category)

    if filter_query:
        products = products.filter(Q(name__icontains=filter_query) | Q(main_category__name__icontains=filter_query) | Q(description__icontains=filter_query))
    if not products.exists():
        messages.info(request, "No products found matching your criteria.")

    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'promoted_products': promoted_products,
        'filter_input': filter_query,
        'category': category,
        'page_obj': page_obj
        }
    return render(request, 'store/products.html', context)





def product_detail(request, product_id):
    """
    product_detail taken from BoutiqueAdo
    
    """
    product = get_object_or_404(Product, pk=product_id) # Grab all the Product objects
    # The context returned to the view...
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)