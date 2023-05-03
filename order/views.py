import stripe
import json
from django.http import JsonResponse
from django.conf import settings
# import pub_key from settings.py

from .models import OrderItem, Order
# import the Cart class from the cart app
from cart.cart import Cart

# Create your views here.
def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body) # get the data sent from the client
    total_price = 0 # get the total price of the cart

    items = []

    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        # make a dictionary for each item
        obj = {
            'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': product.name,
            },
            'unit_amount': int(product.price * 100),
            },
            'quantity': int(item['quantity']),
            }
        items.append(obj)
        

        stripe.api_key = settings.STRIPE_SECRET_KEY # set the secret key for the Stripe API
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=items,
            mode='payment',
            success_url='http://localhost:8000/cart/success/',
            cancel_url='http://localhost:8000/cart',
            # docs for success_url and cancel_url: https://stripe.com/docs/api/checkout/sessions/create#create_checkout_session-success_url
        )
        payment_intent = session.payment_intent # get the payment intent from the session, explain payment intent: https://stripe.com/docs/api/payment_intents/object
        
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        address = data['address']
        zipcode = data['zipcode']
        place = data['place']
        phone = data['phone']

        order = Order.objects.create(
            user=request.user,
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            address=address, 
            zipcode=zipcode, 
            place=place, 
            phone=phone
          )

        order.payment_intent = payment_intent
        order.paid_amount = total_price
        order.paid = True
        order.save()



        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity
            item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

        # return JSON response
        return JsonResponse({'session': session, 'order': payment_intent})       
       


