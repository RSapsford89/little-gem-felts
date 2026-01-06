from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from store.models import Product, Category

# Create your tests here.
# information from:https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing
# https://docs.djangoproject.com/en/6.0/topics/testing/overview/
class BasketTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='test',
        )
        cls.product=Product.objects.create(
            name='Felted Bag',
            description='A beautiful handmade felted bag',
            price=Decimal('25.99'),
            stock_level=10,
            delivery_cost=Decimal('3.50'),
            main_category=cls.category,
            promoted=False
        )


    def tearDown(self):
        return super().tearDown()
    

class AddToBasketTest(BasketTestCase):

    def TestViewBasket(self):
        """
        given an empty basket (no user additions)
        the basket page is loaded
        when the 'view basket' button is pressed
        the page redirects to basket/basket.html
        the page has no product contents
        """
        response= self.client.get(reverse('basket:view_basket'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')
        # an empty basket should return default values.
        self.assertEqual(response.context['product_count'],0)
        self.assertEqual(response.context['basket_items'],[])
        self.assertEqual(response.context['total'],0)
        self.assertEqual(response.context['delivery'],0)
        self.assertEqual(response.context['grand_total'],0)

    def TestAddItem(self):
        """
        the basket is empty
        when the user adds an item in stock
        then the item should be added to the basket
        """
        product = self.product
        quantity =2

        add_item = self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data={'quantity':quantity}
        )

        response = self.client.get(reverse('basket:view_basket'))

        session = self.client.session
        basket = session.get('basket',{})

        self.assertNotEqual(response.context['basket_items'],[])
        self.assertEqual(response.context['total'],Decimal('51.98'))
        self.assertEqual(response.context['delivery'],3.5)
        self.assertEqual(response.context['grand_total'],Decimal('55.48'))
        self.assertEqual(response.context['product_count'],2)