"""
Docstring for basket.contexts
This program should handle the basket  calculations
and contents, delivery and totals.
"""
def basket(request):

    subtotal = None
    delivery =  None
    total = None
    basket = [] # needs to fetch the items from the basket when implemented
    highest_delivery = 3.50 # the minimum cost of an order

    for each item in basket[cost,qty]:
        subtotal += (item.cost * qty)

    # for loop through all the items to determine the highest delivery cost to use
    for delivery_cost in itemList:
        if delivery_cost > highest_delivery:
            highest_delivery = delivery_cost

