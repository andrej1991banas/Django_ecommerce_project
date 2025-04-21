from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingAddressForm, PaymentForm
from .models import ShippingAddress
from member.models import Member
from django.contrib import messages




def payment_success(request):
    return render(request, 'order/payment_success.html', {})



def checkout(request):
    # get the Cart
    cart = Cart(request)
    cart_products = cart.get_cart_prods
    quantities = cart.get_cart_qty
    totals = cart.cart_total()

    if request.user.is_authenticated:
        #checkout as User
        shipping_user = ShippingAddress.objects.get(shipping_user=request.user.id)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        context ={"cart_products": cart_products,
                       "totals": totals,
                       "quantities": quantities,
                       "shipping_form": shipping_form
                       }
        return render(request, "order/checkout.html", context)

    else:
        #checkout as guest
        shipping_form = ShippingAddressForm(request.POST or None)
        context = {"cart_products": cart_products,
                   "totals": totals,
                   "quantities": quantities,
                   "shipping_form": shipping_form
                   }
        return render(request, "order/checkout.html", context)


def billing_info(request):

    if request.POST:
        # get the cart
        cart = Cart(request)
        cart_products = cart.get_cart_prods
        totals = cart.cart_total()
        quantities = cart.get_cart_qty
        billing_form = PaymentForm(request.POST)
        #chcek to see if user is looged in
        if request.user.is_authenticated:
            member = Member.objects.get(user=request.user)
            #fget billing info



            context = {"cart_products": cart_products,
                       "totals": totals,
                       "quantities": quantities,
                       "shipping_info": request.POST,
                       "member": member.phone_number,
                       "billing_form": billing_form
                       }
            return render(request, 'order/billing_info.html', context)
        else:
            pass

            shipping_form= request.POST
            context = {"cart_products": cart_products,
                           "totals": totals,
                           "quantities": quantities,
                           "shipping_info": request.POST,

                           "billing_form": billing_form
                           }
            return render(request, 'order/billing_info.html', context)
    else:
         messages.success(request, "Access Denied")
         return redirect("index")



def payment_info(request):
    billing_form = PaymentForm(request.POST)
    context = {
        "billing_form" : billing_form
    }
    return render(request, 'order/payment_info.html', context)
