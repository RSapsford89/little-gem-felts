from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from store.models import Product

# Create your views here.

@staff_member_required
def product_management(request):
    """
    View to display all products for admin management.
    Requires staff/admin privileges.
    """
    products = Product.objects.all().select_related('main_category')
    
    context = {
        'products': products,
    }
    
    return render(request, 'management/product_management.html', context)
