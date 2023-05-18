from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .cart import Cart
from django.contrib.auth.decorators import login_required
from product.models import Product
from django.conf import settings
# Create your views here.
def add_to_cart(request, product_id):
    cart = Cart(request) # create a new cart object passing it the request object
    cart.add(product_id) # add a product to the cart
    print('cart', cart.cart)
    return render(request, 'cart/menu_item.html') # redirect the user to the cart details page

def cart(request):
  
    return render(request, 'cart/index.html')

def success(request):
    return render(request, 'cart/success.html')


def update_cart(request, product_id, action):
    cart = Cart(request)
    if action == 'increment':
      
        cart.add(product_id, 1, True) # add one to the quantity
        cart.save()
    else:
      
        cart.add(product_id, -1, True) # remove one from the quantity
        # check if the quantity is 0, if so, remove the item from the cart
          # if the quantity is now 0, remove the item from the cart
        if cart.get_item(product_id) is None or cart.get_item(product_id)['quantity'] == 0:
            cart.remove(product_id)
       
    # get the product object from the database including the product id
    product = Product.objects.get(pk=product_id)
    # get the product object photo set
    photo = product.photo_set.first() # get the first photo in the set from the database
    
    quantity = cart.get_item(product_id)['quantity'] # get the quantity of the updated product


    item = {
        'product': {
        'id': product_id,
        'name': product.name,
        'image_url': photo.url,
        'price': product.price,
        },
        'id': product_id,
        'total_price': (product.price * quantity),
        'quantity': quantity,
    }
    print('item.image_url', item['product']['image_url'])
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
    cart = Cart(request)
    total_cost = 0
    # total_cost = cart.get_total_cost()
    # find the sum of the total cost of all items in the cart
    for item in cart:
        total_cost += item['total_price']
    return render(request, 'cart/partials/cart_total.html', {'total_cost': total_cost})

