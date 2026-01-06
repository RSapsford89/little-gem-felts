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
        cls.product = Product.objects.create(
            name='Felted Bag',
            description='A beautiful handmade felted bag',
            price=Decimal('25.99'),
            stock_level=10,
            delivery_cost=Decimal('3.50'),
            main_category=cls.category,
            promoted=False
        )
        cls.product_single_stock = Product.objects.create(
            name='Felt Kit',
            description='Felt kit of sheep at sunset',
            price=Decimal('28.00'),
            stock_level=2,
            delivery_cost=Decimal('3.00'),
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
        and a success message should be displayed
        """
        product = self.product
        quantity =1

        add_item = self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data={'quantity':quantity}
        )

        response = self.client.get(reverse('basket:view_basket'))

        session = self.client.session
        basket = session.get('basket',{})
        self.assertIn(str(product.id),basket)
        self.assertEqual(basket[str(product.id)],  quantity)

        # Test 2: Check CONTEXT basket (processed data from context processor)
        self.assertNotEqual(response.context['basket_items'], [])
        self.assertEqual(response.context['total'], Decimal('25.99'))
        self.assertEqual(response.context['delivery'], Decimal('3.50'))
        self.assertEqual(response.context['grand_total'], Decimal('29.49'))
        self.assertEqual(response.context['product_count'], 1)
        
        # Test 3: Verify basket item details
        basket_item = response.context['basket_items'][0]
        self.assertEqual(basket_item['product'].id, product.id)
        self.assertEqual(basket_item['quantity'], quantity)
        self.assertEqual(basket_item['total'], Decimal('25.99'))

    def AddMultipleItems(self):
        """
        When the basket is empty
        when the user adds 2 in stock items
        then both items should be in the basket
        totals should be for both items
        """
        product = self.product
        product2 = self.product_single_stock
        quantity = 1
        quantity2 = 1

        # the first item is added
        self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data={'quantity': quantity}
        )
        #the second item is added
        self.client.post(
            reverse('basket:add_to_basket', args=[product2.id]),
            data={'quantity': quantity2}
        )

        response = self.client.get(reverse('basket:view_basket'))

        session = self.client.session
        basket = session.get('basket',{})
        # test the item id's and qty are present
        self.assertIn(str(product.id), basket)
        self.assertIn(str(product2.id), basket)