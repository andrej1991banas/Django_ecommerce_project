from product.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session

        #get the current session key if exists
        cart=self.session.get('session_key')

        #if user is new, no session key and create one
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}

        #make sur cart is available on all paes of site
        self.cart=cart


    def add(self, product):
        product_id= str(product.id)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]= {'price': str(product.price)}

        self.session.modified = True


    def __len__(self):
        return len(self.cart)


    def get_cart_prods(self):
        #get IDs from Cart
        product_ids= self.cart.keys() #jquerry returning dict with id. product as key

        #use IDs to look for products in cart
        products= Product.objects.filter(id__in=product_ids)

        #return those looked up products
        return products


    def delete(self, product):
        product_id = str(product)
        #delete from dict/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True