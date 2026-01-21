from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from store.forms import ProductForm
from store.models import Product

# Create your views here.

@staff_member_required
def product_management(request):
    """
    View to display all products for admin
    Requires staff/admin privileges via decorator
    """
    # grab all the Product!
    products = Product.objects.all().select_related('main_category')    
    context = {
        'products': products,
    }
    
    return render(request, 'management/product_management.html', context)

@staff_member_required
def edit_product(request,product_id):
    """
    View to edit the selected item from the product list
    Uses staff decorator
    """
    product = get_object_or_404(Product,pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('management:product_management')
    else:
        form = ProductForm(instance=product)
    context = {
        'product': product,
        'form': form,
        'edit': True,

    }
    return render(request,'management/product_add_edit.html', context)

@staff_member_required
def add_product(request):
    """
    View to add a new product to the product list
    Use staff decorator
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:product_management')
    else:
        form = ProductForm()
    context ={
        'form': form,
        'edit':False,
    }
    return render(request, 'management/product_add_edit.html', context)