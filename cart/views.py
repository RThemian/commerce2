from django.shortcuts import render
from .cart import Cart
from django.contrib.auth.decorators import login_required
from product.models import Product
# Create your views here.
def add_to_cart(request, product_id):
    cart = Cart(request) # create a new cart object passing it the request object
    cart.add(product_id) # add a product to the cart

    return render(request, 'cart/menu_item.html') # redirect the user to the cart details page

def cart(request):
   
    # cart = Cart(request)
    # cart_items = cart.get_cart_items()
    return render(request, 'cart/index.html')

def update_cart(request, product_id, action):
    cart = Cart(request)
    if action == 'increment':
        cart.add(product_id, 1, True) # add one to the quantity
    else:
        cart.add(product_id, -1, True) # remove one from the quantity

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)

    item = {
        'product': {
        'id': product_id,
        'name': product.name,
        'image': product.image,
        'price': product.price,
        },
        'total_price': (product.price * quantity) / 100,
        'quantity': quantity,
    }
    response = render(request, 'cart/partials/cart_item.html', {'item': item})

    response['HX-Trigger'] = 'update-menu-cart' # trigger the cart.update event on the client side

    return response


@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')

def hx_menu_item(request):
    return render(request, 'cart/menu_item.html')

def get_item(self, product_id):
    return self.cart[str(product_id)]

def hx_cart_total(request):
  
    return render(request, 'cart/partials/cart_total.html')

