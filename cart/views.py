from django.shortcuts import render
from .cart import Cart
# Create your views here.
def add_to_cart(request, product_id):
    cart = Cart(request) # create a new cart object passing it the request object
    cart.add(product_id) # add a product to the cart

    return render(request, 'cart/menu_item.html') # redirect the user to the cart details page

def cart(request):
   
    # cart = Cart(request)
    # cart_items = cart.get_cart_items()
    return render(request, 'cart/index.html')

def checkout(request):
    return render(request, 'cart/checkout.html')
