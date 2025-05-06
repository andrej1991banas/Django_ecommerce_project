from venv import create

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingAddressForm, PaymentForm
from .models import ShippingAddress
from member.models import Member
from product.models import Product
from django.contrib import messages
from .models import Order, OrderItems
import datetime




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
        shipping_form = ShippingAddressForm(request.POST, instance=shipping_user)
        if shipping_form.is_valid():
            shipping_address = shipping_form.save(commit=False)
            shipping_address.shipping_user = request.user  # Assign the currently logged-in user
            shipping_address.save()  # Save the instance to the database

            messages.success(request, "Your shipping address has been saved successfully!")
            return redirect("billing-info")
        else:
            # Add messages for form errors
            messages.success(request, "Fill your shipping address")
            for error in shipping_form.errors.values():
                messages.error(request, error)
            shipping_form = ShippingAddressForm(instance=shipping_user)

        context ={"cart_products": cart_products,
                       "totals": totals,
                       "quantities": quantities,
                       "shipping_form": shipping_form
                       }
        return render(request, "order/checkout.html", context)

    else:
        #checkout as guest

        shipping_form = ShippingAddressForm(request.POST)
        if request.method == 'POST' and shipping_form.is_valid():
            # Save the shipping address without associating it to a user
            shipping_form.save()
            messages.success(request, "Your shipping address has been saved successfully!")
            return redirect("billing-info")
            # else:
            #     # Provide feedback on invalid form submission
            #     if request.method == 'POST':
            #         messages.success(request, "Please fill in your shipping address correctly.")
            #         for error in shipping_form.errors.values():
            #             messages.error(request, error)
        else:
            messages.success(request, "Please fill in your shipping address correctly.")
            shipping_form = ShippingAddressForm()

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


        #create a session with Shipping and Cart info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #chcek to see if user is logged in
        if request.user.is_authenticated:
            member = Member.objects.get(user=request.user)
            # billing info and form
            billing_form = PaymentForm(request.POST)


            context = {"cart_products": cart_products,
                       "totals": totals,
                       "quantities": quantities,
                       "shipping_info": request.POST,
                       "member": member.phone_number,

                       }
            return render(request, 'order/billing_info.html', context)

        else:
            #not logged in so exists as a guest
            billing_form = PaymentForm(request.POST)
            context = {"cart_products": cart_products,
                           "totals": totals,
                           "quantities": quantities,
                           "shipping_info": request.POST,}

            return render(request, 'order/billing_info.html', context)
    else:
         messages.success(request, "Access Denied")
         return redirect("index")



def payment_info(request):
    billing_form = PaymentForm(request.POST)

    # If the form is valid
    if billing_form.is_valid():
        # Access the cleaned data from the valid form
        payment_data = billing_form.cleaned_data

        # You can process `payment_data` here, e.g., saving it to the database
        # or sending it to another view.
        # print("Validated Payment Data:", payment_data)  # Debugging purpose

        # Redirect to the next step in the order process
        return redirect("process-order")

    # If the form is invalid
    else:
        messages.success(request, "Fill in your payment information correctly.")
        for error in billing_form.errors.values():
            messages.error(request, error)

    # Render the form again with errors displayed
    context = {
        "billing_form": billing_form
    }
    return render(request, 'order/payment_info.html', context)



def process_order(request):

    if request.POST:
        # Get billing info or nothing

        billing_form = PaymentForm(request.POST)
        # get a instance of the Cart
        cart = Cart(request)
        cart_products = cart.get_cart_prods()
        quantities = cart.get_cart_qty()

        #get all data we have till this point )shipping and cart data)
        my_shipping = request.session.get('my_shipping')

        # gather Order Info
        #Create shipping address from session info as a text field
        shipping_label = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        full_name =f"{my_shipping['shipping_first_name']}' '{my_shipping['shipping_last_name']}"
        email=f"{my_shipping['shipping_email']}"
        amount_paid = cart.cart_total()

        #gather Order Info
        if request.user.is_authenticated:
            #logged in user
            member = Member.objects.get(user=request.user)
            #Cerate Order

            create_order = Order(shipping_label=shipping_label, full_name=full_name, email=email, amount_paid=amount_paid)
            create_order.save()

            # Add the member to the Many-to-Many field
            create_order.member.add(member)

            #add Order Item

            #Get Product info
            for product in cart_products:
                # get the IDs
                product_id = product.id
                # get product price
                price = product.price

                # get Quantity
                for key, value in quantities.items():
                    if int(key) == product.id:

                        # Create Order Item
                        #get Order ID from instance created order right above
                        create_order_item = OrderItems(order=create_order, products=product, price=price, quantity=value)
                        create_order_item.save()

            #Delete our persisted Cart after purchase and confirmation of the order
            for key in list(request.session.keys()):
                if key.startswith('session_key'):
                    #Delete the session
                    del request.session[key]
                    request.session.modified = True


            # delete Cart from the Database (old_cart filed)
            current_user = Member.objects.filter(user__id=request.user.id)
            # delete shopping cart for current_user
            current_user.update(old_cart="")

            messages.success(request, f"Order Created Successfully! Thank you, {create_order.full_name} for shopping with us! Your order number is:{create_order.id}")
            context = {}
            return render(request, "user_auth/index.html", context)

        else:
            #not logged in
            # Create Order
            create_order = Order(shipping_label=shipping_label, full_name=full_name, email=email,
                                 amount_paid=amount_paid)
            create_order.save()
            # add Order Item
            # Get Product info
            for product in cart_products:
                # get the IDs
                product_id = product.id
                # get product price
                price = product.price

                # get Quantity
                for key, value in quantities.items():
                    if int(key) == product.id:
                        # Create Order Item
                        # get Order ID from instance created order right above
                        create_order_item = OrderItems(order=create_order, products=product, price=price,
                                                       quantity=value)
                        create_order_item.save()

            # Delete our persisted Cart after purchase and confirmation of the order
            for key in list(request.session.keys()):
                if key.startswith('session_key'):
                    # Delete the session
                    del request.session[key]
                    request.session.modified = True


            messages.success(request,
                             f"Order Created Successfully! Thank you for shopping with us! Your order number is:{create_order.id}")

            context = {}
            return render(request, "user_auth/index.html", context)
    else:
        messages.success(request, "Access Denied")
        return redirect("index")





#Admin Dashboard view
def status_shipped(request):
    if request.user.is_authenticated and request.user.is_superuser:
        #Check if the current User is Superuser (Admin)
        orders = Order.objects.filter(status=True).order_by('-date_shipped')
        if request.POST:
            shipped = request.POST['shipping_status']
            num = request.POST['num']
            #Get the Order
            order=Order.objects.filter(id=num)
            # update status with correct date of shipping
            now = datetime.datetime.now()

            # update status of the order
            order.update(status=False)

            messages.success(request, "Shipping status updated to NOT SHIPPED")
            return redirect("status-shipped")

        context = {"orders": orders}
        return render(request, 'order/status_shipped.html', context)
    else:
        #user is not a Admin user
        messages.success(request, "You do not have permissions")
        return redirect("index")


#Admin Dashboard view
def status_not_shipped(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Check if the current User is Superuser (Admin)
        orders = Order.objects.filter(status=False).order_by('-created_at')

        if request.POST:
            shipped = request.POST['shipping_status']
            num = request.POST['num']
            #Get the Order
            order=Order.objects.filter(id=num)
            # update status with correct date of shipping
            now = datetime.datetime.now()

            # update status of the order
            order.update(status=True, date_shipped=now)

            messages.success(request, "Shipping status updated to SHIPPED")
            return redirect("status-not-shipped")


        context = {"orders": orders}
        return render(request, 'order/status_not_shipped.html', context)
    else:
        # user is not a Admin user
        messages.success(request, "You do not have permissions")
        return redirect("index")



def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        #get needed Order
        order = Order.objects.get(id=pk)
        #Get the order Items
        items = OrderItems.objects.filter(order=pk)

        if request.POST:
            shipped = request.POST['shipping_status']
            #Check if true or false
            if shipped == "true":
                #Get the order
                order = Order.objects.filter(id=pk)

                #update status with correct date of shipping
                now = datetime.datetime.now()

                # update status of the order
                order.update(status=True, date_shipped=now)

                messages.success(request, "Shipping status updated to SHIPPED")
                return redirect("status-shipped")
            else:
                order = Order.objects.filter(id=pk)
                # update status of the order
                order.update(status=False)

                messages.success(request, "Shipping status updated to  NOT SHIPPED")
                return redirect("status-not-shipped")


        context = {"order": order,
                   "items": items}
        return render(request, 'order/order.html', context)
    else:
        # user is not a Admin user
        messages.success(request, "You do not have permissions")
        return redirect("index")


def order_details(request, pk):
    if request.user.is_authenticated:
        #get needed Order
        order = Order.objects.get(id=pk)
        #Get the order Items
        items = OrderItems.objects.filter(order=pk)

        context = {"order": order,
                   "items": items}
        return render(request, 'order/order_details.html', context)
    else:
        # user is not an authenticated user
        messages.success(request, "You are not logged in")
        return redirect("index")




