from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
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
        cls.product_no_stock = Product.objects.create(
            name='lamp',
            description='I like lamp',
            price=Decimal('75.00'),
            stock_level=0,
            delivery_cost=Decimal('5.00'),
            main_category=cls.category,
            promoted=False
        )
        cls.product_increment = Product.objects.create(
            name='lamp',
            description='I like lamp',
            price=Decimal('75.00'),
            stock_level=3,
            delivery_cost=Decimal('5.00'),
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
        response = self.client.get(reverse('basket:view_basket'))
        
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
        print(f"basket contents:{basket}")
        print(f"context basket contents:{response.context['basket_items']}")
        # test the item id's and qty are present
        self.assertIn(str(product.id), basket)
        self.assertIn(str(product2.id), basket)
        self.assertEqual(basket[str(product.id)], quantity)
        self.assertEqual(basket[str(product2.id)], quantity2)

        # qty 1 cost 25.99 del 3
        # qty 1 cost 28 del 3.50 <- highest used
        # total 53.99
        # grand total 57.49
        self.assertEqual(response.context['total'], Decimal('53.99'))
        self.assertEqual(response.context['delivery'], Decimal('3.50'))
        self.assertEqual(response.context['grand_total'], Decimal('57.49'))
        self.assertEqual(response.context['product_count'], 2)

    def oosItem(self):
        """
        when an item is out of stock
        then a user tries to add to basket
        the item is not added 
        and a message is displayed notifying OOS
        """
        # id = 3
        product = self.product_no_stock
        quantity = 1

        self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data = {'quantity': quantity}
        )
        
        response = self.client.get(reverse('basket:view_basket'))
        session = self.client.session
        messages = list(get_messages(response.wsgi_request))
        basket = session.get('basket',{})

        print(messages)
        print(f"basket contents:{basket}")
        print(f"context basket contents:{response.context['basket_items']}")

        self.assertEqual(str(messages[0]), f'This item only has {product.stock_level} left')
        self.assertIsNot(str(product.id), basket)

    def qtyInBasketGreaterThanStock(self):
        """
        when an item in the basket > remaining stock
        then the user tries to add additional item
        the item qty is updated to == remaining stock
        and a message informs the user there is 'only <x> stock'
        
        """
        product = self.product_increment
        quantity = 2

        # add the item once
        self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data = {'quantity': quantity}
        )

        session = self.client.session
        basket = session.get('basket',{})
        print(f"First basket contents:{basket}")
        firstResponse = self.client.get(reverse('basket:view_basket'))
        firstMessages = list(get_messages(firstResponse.wsgi_request))
        self.assertEqual(len(firstMessages), 1, "Should 1 message after first addition")
        self.assertEqual(str(firstMessages[0]), f'Added {quantity} of {product.name} to the basket')
        
        print("---end first section---")

        # add the same item again (exceeding stock levels)
        self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data = {'quantity': quantity}
        )

        session = self.client.session
        basket = session.get('basket',{})
        response = self.client.get(reverse('basket:view_basket'))
        messages = list(get_messages(response.wsgi_request))

        print(f'Second messages: {messages}')
        print(f"Second basket contents:{basket}")
        print(f"context basket contents:{response.context['basket_items']}")

        # check content of session bag
        # check content of context bag
        # check messages
        self.assertIn(str(product.id), basket)
        self.assertEqual(basket[str(product.id)], product.stock_level, f"Basket should be capped at stock level {product.stock_level}")
        self.assertLessEqual(basket[str(product.id)], product.stock_level, f"Basket quantity {basket[str(product.id)]} exceeds stock level {product.stock_level}")        
        # Check the error message is displayed
        self.assertEqual(str(messages[1]), f'Only {product.stock_level} of {product.name} is available. {product.stock_level} has been updated.')

class updateBasket(BasketTestCase):
    def testUpdateInput(self):
        """
        when there is an item in the basket
        the qty input displays the current qty
        then the user presses the plus button
        and the input's display is increased by 1
        and the item qty increases by 1 in the session basket & context
        """

        product = self.product
        quantity = 1

        # add the item once
        self.client.post(
            reverse('basket:add_to_basket', args=[product.id]),
            data = {'quantity': quantity}
        )

        # view the basket
        response = self.client.get(reverse('basket:view_basket'))

        # unmodifed by button press
        session = self.client.session
        basket = session.get('basket',{})
        print(f"First basket contents:{basket}")
        firstResponse = self.client.get(reverse('basket:view_basket'))
        firstMessages = list(get_messages(firstResponse.wsgi_request))
        self.assertEqual(len(firstMessages), 1, "Should 1 message after first addition")
        self.assertEqual(str(firstMessages[0]), f'Added {quantity} of {product.name} to the basket')