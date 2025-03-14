from .cart import Cart

#cart will work on every page of the site

def cart(request):
    #return default data from cart
    return {'cart': Cart(request)}
