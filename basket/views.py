from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
import json
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
    request.session.modified = True
    #print(basket)
    # redirect_url = request.POST.get('')
    return redirect('basket:view_basket')

def update_basket(request, product_id):
    """
    Docstring for update_basket
    update the quantity of items in the basket
    """
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, pk=product_id)# obj from DB
            basket = request.session.get('basket',{})
            data = json.loads(request.body)
            quantity = int(data.get('quantity')) # get qty from json obj
            # if prod id is in basket
                # find the requestedQty
                # stock is available and less than max... 
                # if available, set basket to requestedQty
                # addition: could add another model field 'preOrder' which = stock level - requested
                # then, if preOrder = > stocklevel, can't add the stock
            if str(product_id) in basket:
                if quantity <= 0:
                    # if you request 0 or negative
                    del basket[str(product_id)]
                    request.session['basket'] = basket
                    request.session.modified = True
                    from basket.contexts import basket_contents
                    context = basket_contents(request)
                    return JsonResponse({
                        'success': True,
                        'product_count': context['product_count'],
                        'total': str(context['total']),
                        'delivery': str(context['delivery']),
                        'grand_total': str(context['grand_total']),
                        'message': f'Removed {product.name} from the basket'
                    })
                elif product.stock_level > 0 and quantity <= product.stock_level: 
                    basket[str(product_id)] = quantity # make prodId's value = quantity from json
                    request.session['basket'] = basket
                    request.session.modified = True
                    from basket.contexts import basket_contents
                    context = basket_contents(request)
                    return JsonResponse({
                        'success': True,
                        'product_count': context['product_count'],
                        'total': str(context['total']),
                        'delivery': str(context['delivery']),
                        'grand_total': str(context['grand_total']),
                        'message': f'Updated {product.name} quantity to: {quantity}',
                    })
                elif quantity > product.stock_level:
                    # if stock_level < quantity ?
                    # there is stock, but not enough for the customer's request
                    # set the basket to remaining stock level
                    basket[str(product_id)] = product.stock_level
                    request.session['basket'] = basket
                    request.session.modified = True
                    from basket.contexts import basket_contents
                    context = basket_contents(request)
                    return JsonResponse({
                        'success': True,
                        'product_count': context['product_count'],
                        'total': str(context['total']),
                        'delivery': str(context['delivery']),
                        'grand_total': str(context['grand_total']),
                        'message': f'Only {product.stock_level} available. Updated to: {product.stock_level}',
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Product no in basket'
                }, status=404)
            
        except Exception as error:
            return JsonResponse({
                'success': False,
                'message': f'Error updating item! {str(error)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=400)


    # general idea taken from Boutique Ado project.
    # used AI to assist with the JSON formatting
    # so the AJAX response would work
def remove_basket(request, product_id):
    """
    Remove an item from the basket and update totals.
    Using AJAX with jsonresponse to update basket context
    """
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, pk=product_id)
            basket = request.session.get('basket',{})
            if str(product_id) in basket:
                del basket[str(product_id)]
                request.session['basket'] = basket
                request.session.modified = True
                from basket.contexts import basket_contents
                context = basket_contents(request)
                return JsonResponse({
                    'success':True,
                    'product_count': context['product_count'],
                    'total': str(context['total']),
                    'delivery':str(context['delivery']),
                    'grand_total':str(context['grand_total']),
                    'message': f'Removed {product.name} from the basket'
                })
            else:
                return JsonResponse({
                    'success':False,
                    'message':'Unable to remove or find item'
                }, status=404)
            
        except Exception as error:
            return JsonResponse({
                'success': False,
                'message': f'Error removing item! {str(error)}'
            }, status=500)
    return JsonResponse({
        'success': False,
        'message':'invalid request method'
    }, status=400)



def view_basket(request):
    basket = request.session.get('basket',{})
    #print(basket)
    return render(request, 'basket/basket.html')