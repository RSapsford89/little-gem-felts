from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from store.models import Product  
# Create your views here.

def add_to_basket(request, product_id):
    """
    Docstring for add_to_basket
    When a user clicks on 'add' the basket is updated
    :param request: Description
    :param product_id: from prodduct_detail page 
    """
    if request.method == 'POST': # this ccould be a decorator instead?
        product = get_object_or_404(Product, pk=product_id) # get the obj from DB
        quantity = int(request.POST.get('quantity')) # get qty from  page, cast
        basket = request.session.get('basket', {}) # get session basket

        if product.stock_level > 0 and quantity <= product.stock_level: # stock is available and adding <= stock available
            if str(product_id) in basket: # is it in the basket already?
                if (basket[str(product_id)] + quantity) > product.stock_level: #asking for too much
                    basket[str(product_id)] = product.stock_level
                    messages.error(request, f'Only {product.stock_level} of {product.name} is available. {product.stock_level} has been updated.')
                else: # asking for available amount
                    basket[str(product_id)] += quantity
                    messages.success(request, f' {product.name} updated to {quantity}.')
            else: # it isn't in the basket
                basket[str(product_id)] = quantity
                messages.success(request, f'Added {quantity} of {product.name} to the basket')
        else:
            messages.error(request, f'This item only has {product.stock_level} left')
    else:

        return redirect('store:store')
    
    request.session['basket'] = basket
    request.session.modified=True
    #print(basket)
    # redirect_url = request.POST.get('')
    return redirect('basket:view_basket')

def update_basket(request):
    """
    Docstring for update_basket
    update the quantity of items in the basket
    :param request: Description
    """
def remove_basket(request):
    return()


def view_basket(request):
    basket = request.session.get('basket',{})
    #print(basket)
    return render(request,'basket/basket.html')