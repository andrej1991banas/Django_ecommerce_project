from product.models import Product
from member.models import Member

class Cart:
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request

        #get the current session key if exists
        cart=self.session.get('session_key')

        #if user is new, no session key and create one
        if 'session_key' not in request.session:
            cart=self.session['session_key'] = {}

        #make sure cart is available on all pages of site
        self.cart=cart


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True  # Mark the session as modified

        # Save the updated cart to the database for logged-in users
        if self.request.user.is_authenticated:
            current_profile = Member.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")  # Convert single quotes to double quotes for valid JSON
            current_profile.update(old_cart=str(carty))

            self.request.user.member.save()


    def add(self, product, quantity ):
        product_id= str(product.id)
        product_qty = quantity

        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id]= {'price': str(product.price)}
            self.cart[product_id] = product_qty

        self.session.modified = True

        #deal with logged-in user
        if self.request.user.is_authenticated:
            #get current user profile
            current_profile = Member.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty= carty.replace("\'", "\"")

            #save our variable "carty" into Member model
            current_profile.update(old_cart=str(carty))
            self.request.user.member.save()


    def __len__(self):
        return len(self.cart)



    def get_cart_prods(self):
        #get IDs from Cart
        product_ids= self.cart.keys() #jquerry returning dict with id. product as key

        #use IDs to look for products in cart
        products= Product.objects.filter(id__in=product_ids)

        #return those looked up products
        return products



    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get the actual cart
        act_cart = self.cart

        # update dict/cart
        act_cart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            #get current user profile
            current_profile = Member.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty= carty.replace("\'", "\"")
            #save our variable "carty" into Member model
            current_profile.update(old_cart=str(carty))

        updated_cart = self.cart
        return updated_cart



    def delete(self, product):
        product_id = str(product)
        #delete from dict/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        # deal with logged-in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_profile = Member.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")

            # save our variable "carty" into Member model
            current_profile.update(old_cart=str(carty))


    def cart_total(self):
        # Get product IDs from the cart (keys of the dictionary)
        products_ids = self.cart.keys()
        # Query database for the corresponding products
        products = Product.objects.filter(id__in=products_ids)

        #start counting from 0
        total = 0
        items_price = 0
        for key in products:
            for product in products:
                # The quantity of the current product in the cart
                product_id_str = str(product.id)  # Convert product ID to match dictionary keys
                if product_id_str in self.cart:
                    quantity = self.cart[product_id_str]  # Get the quantity

                    # Multiply product price by quantity
                    total += product.price * quantity

        return total



    def get_cart_qty(self):
        quantities= self.cart
        return quantities