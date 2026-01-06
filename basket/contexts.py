from django.shortcuts import get_object_or_404
from store.models import Product
def basket_contents(request):
    """
    Docstring for basket.contexts
    This program should handle the basket  calculations
    and contents, delivery and totals.
    """
    basket_items=[]
    product_count = 0
    total = 0
    delivery = 0 # the minimum cost of an order
    
    basket = request.session.get('basket', {}) # needs to fetch the items from the basket when implemented

    for product_id, quantity in basket.items():
        product = get_object_or_404(Product, pk=product_id)
        product_count =+ quantity
        product_total = quantity * product.price
        total += product_total

        if product.delivery_cost > delivery:
            delivery =  product.delivery_cost        

        basket_items.append({
            'product_id': product_id,
            'quantity':quantity,
            'product':product,
            'product_count':product_count,
            'total':total,
        })
    grand_total = total + delivery
        # subtotal += (item.cost * qty)
    return {
        'basket_items':basket_items,
        'product_count':product_count,
        'total':total,
        'delivery':delivery,
        'grand_total':grand_total,
    }


