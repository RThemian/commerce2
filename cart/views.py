from django.shortcuts import render
from .cart import Cart
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.conf import settings
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
        print('action', action)
        cart.add(product_id, 1, True) # add one to the quantity
        cart.save()
        print('cart', cart.cart)
    else:
        print('action', action)
        print('cart_before', cart.cart)
        cart.add(product_id, -1, True) # remove one from the quantity
        # check if the quantity is 0, if so, remove the item from the cart
          # if the quantity is now 0, remove the item from the cart
        if cart.get_item(product_id) is None or cart.get_item(product_id)['quantity'] == 0:
            cart.remove(product_id)
       
        
    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)['quantity'] # get the quantity of the updated product


    item = {
        'product': {
        'id': product_id,
        'name': product.name,
        'image': product.image,
        'price': product.price,
        },
        'total_price': (product.price * quantity),
        'quantity': quantity,
    }
    response = render(request, 'cart/partials/cart_item.html', {'item': item})

    response['HX-Trigger'] = 'update-menu-cart' # trigger the cart.update event on the client side

    return response


@login_required
def checkout(request):
    pub_key = settings.STRIPE_PUBLIC_KEY
    # where is this used
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

def hx_menu_item(request):
    return render(request, 'cart/menu_item.html')



def hx_cart_total(request):
  
    return render(request, 'cart/partials/cart_total.html')