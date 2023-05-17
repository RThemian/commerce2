from django.conf import settings

from product.models import Product, Photo


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            product = Product.objects.get(pk=p)
            photo = Photo.objects.filter(product=product).first()
            image_url = photo.url if photo else None
            self.cart[p]['product'] = product
            self.cart[p]['image_url'] = image_url

        for item in self.cart.values():
            item['total_price'] = int(item['product'].price * item['quantity'])
            yield item


    def __len__(self):
        return max(0, sum(item['quantity'] for item in self.cart.values()))


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)
        print('self.cart', self.cart)
        if product_id not in self.cart:
            print('product id not in cart')
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
    # check on convergent id for item and product
        if update_quantity:
            print('update quantity!!!')
            self.cart[product_id]['quantity'] += int(quantity)
            print(self.cart[product_id]['quantity'])
        else:
            self.cart[product_id]['quantity'] += int(quantity)

        if self.cart[product_id]['quantity'] == 0:
            self.remove(product_id)
        self.save()


    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        print('cart', self.cart)
        return int(sum(item['product'].price * item['quantity'] for item in self.cart.values()))

    def get_item(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return {'quantity': 0, 'id': product_id}
