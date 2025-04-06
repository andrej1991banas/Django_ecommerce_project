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

        #make sur cart is available on all paes of site
        self.cart=cart


    def db_add(self, product):
        product_id = str(product.id)
        # product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}

        self.session.modified = True

        # deal with logged-in user
        if self.request.user.is_authenticated:
            # get current user profile
            current_profile = Member.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")

            # save our variable "carty" into Member model
            current_profile.update(old_cart=str(carty))


    def add(self, product):
        product_id= str(product.id)
        # product_qty = str(quantity)


    #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]= {'price': str(product.price)}

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
        #get product IDs
        products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=products_ids)
        price_total = self.cart
        #start counting from 0
        total = 0
        items_price = 0
        for key in price_total:
            for product in products:
                if int(key) == product.id:
                    # Remove euro symbol from the string
                    price_int = price_total[key]['price'].replace('€', '')
                    # Remove thousands separators
                    price_int2 = price_int.replace(',', '')
                    # Convert the cleaned string to a float
                    try:
                        price = float(price_int2)
                    except ValueError:
                        raise ValueError(f"Invalid price value: {price_int}")

                    # Try work with Django MOneyField
                    # item_price = product.price.amount
                    # items_price += item_price
                    total += price
        return total