from django.conf import settings # import the settings file

from product.models import Product

class Cart(object):
    def __init__(self, request):
        self.session = request.session # get the session
        cart = self.session.get(settings.CART_SESSION_ID) # get the cart from the session

        if not cart: # if there is no cart
            cart = self.session[settings.CART_SESSION_ID] = {} # create an empty cart
            # {} represents an empty dictionary to store the cart items
        self.cart = cart

    def __iter__(self):
        for product in self.cart.keys():
            self.cart[str(product)]['product'] = Product.objects.get(pk=product)
            # get the product from the database and store it in the cart
    
    def __len__(self): # return the number of items in the cart
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart # save the cart to the session
        self.session.modified = True # mark the session as modified to make sure it is saved

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id) # convert the product id to a string
        if product_id not in self.cart: # if the product is not in the cart
            self.cart[product_id] = {'quantity': 1, 'id': product_id} # add the product to the cart
        
        if update_quantity: # if the quantity is being updated
            self.cart[product_id]['quantity'] += int(quantity) # update the quantity
            if self.cart[product_id]['quantity'] == 0: # if the quantity is 0
                self.remove(product_id) # remove the product from the cart
        self.save() # save the cart

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
