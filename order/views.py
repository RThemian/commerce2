import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from .models import OrderItem, Order
from cart.cart import Cart

def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)  # get the data sent from the client
    total_price = 0  # get the total price of the cart

    items = []

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity
        total_price += price

        # create a dictionary for each item
        item_data = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': quantity,
        }

        items.append(item_data)

    stripe.api_key = settings.STRIPE_SECRET_KEY  # set the secret key for the Stripe API
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='https://commerce-nov8.herokuapp.com/cart/success/',
        cancel_url='https://commerce-nov8.herokuapp.com/cart/',
    )
    payment_intent = session.payment_intent

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
        order_item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

    return JsonResponse({'session': session, 'order': payment_intent})
