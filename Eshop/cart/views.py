from django.shortcuts import render, get_object_or_404
from product.models import Product
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages



def cart_summary(request):
    #get the Cart
    cart = Cart(request)
    cart_products = cart.get_cart_prods
    quantities = cart.get_cart_qty
    totals = cart.cart_total()

    context = {"cart_products":cart_products,
               "totals": totals,
               "quantities": quantities,
               }
    return render(request, "cart/cart_summary.html", context)


def cart_add(request):
    #get the product into cart
    cart= Cart(request)
    # check if authenticated
    if request.user.is_authenticated:
        if request.POST.get('action')=='post':
            #get data from request
            product_id = int(request.POST.get('product_id'))
            product_qty= int(request.POST.get('product_qty'))
            #lookup for product in DB
            product = get_object_or_404(Product, id=product_id)

            #save to session
            cart.add(product=product, quantity=product_qty)

            #get cart quantity
            cart_quantity = cart.__len__()

            #return response
            response = JsonResponse({'qty':cart_quantity})
            messages.success(request, "You added item to your shopping cart")
            return response
    else:
        if request.POST.get('action') == 'post':
            # get data from request
            product_id = int(request.POST.get('product_id'))
            product_qty = int(request.POST.get('product_qty'))

            # lookup for product in DB
            product = get_object_or_404(Product, id=product_id)


            # save to session
            cart.add(product=product, quantity=product_qty)

            # get cart quantity
            cart_quantity = cart.__len__()

            # return response
            response = JsonResponse({'qty': cart_quantity})
            messages.success(request, "You added item to your shopping cart")
            return response



def cart_delete(request):
    cart=Cart(request)
    #check if authenticated
    if request.user.is_authenticated:
        if request.POST.get('action') == 'post':
           product_id= int(request.POST.get('product_id'))
           cart.delete(product=product_id)

           response = JsonResponse ({'product': product_id})
           messages.success(request, "You deleted item from your shopping cart")
           return response
    else:
        if request.POST.get('action') == 'post':
            product_id = int(request.POST.get('product_id'))
            cart.delete(product=product_id)

            response = JsonResponse({'product': product_id})
            messages.success(request, "You deleted item from your shopping cart")
            return response



def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response= JsonResponse({'product':product_id, 'quantity':product_qty})
        return response

