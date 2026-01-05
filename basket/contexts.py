"""
Docstring for basket.contexts
This program should handle the basket  calculations
and contents, delivery and totals.
"""
def basket_contents(request):
    basket = request.session.get('basket', {})
    subtotal = None
    delivery =  None
    total = None
    highest_delivery = 3.50 # the minimum cost of an order
    try:
        basket = request.session.get('basket', {}) # needs to fetch the items from the basket when implemented
    except KeyError:
        basket={}
    basket_ids=[]
    for product_id, qty in basket.items():
        basket_ids=product_id.append(int(product_id))
        # subtotal += (item.cost * qty)
    return{
        'basket_id':basket_ids,
    }
    # for loop through all the items to determine the highest delivery cost to use
    # for delivery_cost in itemList:
    #     if delivery_cost > highest_delivery:
    #         highest_delivery = delivery_cost

