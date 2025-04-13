from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import ShippingAddress




def payment_success(request):
    return render(request, 'order/payment_success.html', {})


def checkout(request):
    #get the cart
    cart = Cart(request)
    cart_products = cart.get_cart_prods
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #checkout as User
        shipping_user = ShippingAddress.objects.get(shipping_user=request.user.id)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        context ={"cart_products": cart_products,
                   "totals": totals,
                  "shipping_form": shipping_form
                  }
        return render(request, "order/checkout.html", context)

    else:
        #checkout as guest
        shipping_form = ShippingAddressForm(request.POST or None)
        context = {"cart_products": cart_products,
                   "totals": totals,
                   "shipping_form": shipping_form
                   }
        return render(request, "order/checkout.html", context)

