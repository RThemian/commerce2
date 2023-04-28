from django.shortcuts import render, redirect

from .models import OrderItem, Order
# import the Cart class from the cart app
from cart.cart import Cart

# Create your views here.
def start_order(request):
    cart = Cart(request)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        place = request.POST.get('place')
        phone = request.POST.get('phone')

        order = Order.objects.create(user=request.user, first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, place=place, phone=phone)

        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity
            item = OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
       # return redirect to localhost:8000/myaccount
        return redirect('core:myaccount')
    return redirect('cart')

