from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import CreateUserForm, LoginForm, UpdateUserForm, ChangePasswordForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
from product.models import Product, Category
from .models import Member
from cart.cart import Cart
from django.contrib import messages
from django.db.models import Q
import json
from order.forms import ShippingAddressForm
from order.models import ShippingAddress






def homepage(request):
    products= Product.objects.all()

    # template = loader.get_template('user_auth/index.html')

    trips = Product.objects.filter(category__name="Trip")
    context = {'products': products,
               'trips': trips}


    return render(request, 'user_auth/index.html', context)



def login(request):
    form= LoginForm()

    if request.method=="POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username= request.POST.get('username')
            password = request.POST.get('password')
            user= authenticate(request,username=username, password=password) #checking if the username and password does exist

            if user is not None:
                auth.login(request, user)
                #Using Cart data
                current_user = Member.objects.get(user__id= request.user.id)
                #get data from saved cart tangled to the user
                saved_cart = current_user.old_cart

                if saved_cart:
                    #convert to dict with JSON
                    converted_cart = json.loads(saved_cart) #from str to dict

                    #add loaded dict to cart_session
                    cart = Cart(request)
                    for key,value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)

                messages.success(request, "Welcome, you successfully logged in!")
                return redirect("dashboard")

            else:
                return HttpResponse("Invalid username or password")  # Error message for failed login
                # return render(request, 'user_auth/login.html', {'loginform': form})
    context= {'loginform':form}
    return render(request, 'user_auth/login.html', context)



def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)  # Bind POST data to the form
        if form.is_valid():
            # Save the user (and the related Member) via the custom save() method
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect("login")
        else:
            # Add messages for form errors
            messages.success(request, "FIll registration form as required")
            for error in form.errors.values():
                messages.error(request, error)
                form = CreateUserForm()
    else:
        form = CreateUserForm()

    # Render the registration form page
    context = {"registerform": form}
    return render(request, "user_auth/register.html", context)




def dashboard(request):
    # rendering the user profile
    if request.user.is_authenticated:
        current_user = request.user
        current_member = current_user.member
        orders = current_member.orders.all()  # Fetch all orders for this member

        context = {
            'username': current_user.username,  # Username
            'email': current_user.email,  # Email
            'first_name': current_user.first_name,  # First Name
            'last_name': current_user.last_name,  # Last Name
            'country': current_member.country,# Member's location
            'city': current_member.city,# Member's location
            'phone_number': current_member.phone_number,
            'orders': orders,
        }
        return render(request, 'user_auth/dashboard.html', context)

    else:
        messages.success(request, "You must be logged in to access this page")
        return redirect('index')

@login_required (login_url="login") #have to be logged in to view the page
def logout(request):

    auth.logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("index")


def about(request):
    return render(request, 'user_auth/about.html')


def navbar_view(request):
    # Fetch all categories
    categories = Category.objects.all()  # Query all categories

    context = {
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'user_auth/navbar.html', context)



def update_user(request):
    if request.user.is_authenticated:
        # Get the currently logged-in user
        current_user = request.user

        # Get the logged-in user's Member object (via the OneToOne relationship)
        member = current_user.member  # Access the related Member object

        # Get current user's shipping info
        shipping_user = ShippingAddress.objects.get(shipping_user=request.user.id)

        # Initialize UpdateUserForm (for profile details)
        update_form = UpdateUserForm(request.POST or None, instance=member)
        # Initialize ShippingAddressForm (for shipping address details)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        # Flags to track successful updates
        user_updated = False
        shipping_updated = False

        # Handle form POST requests
        if request.method == "POST":
            # 1. Update the Member/User information
            if update_form.is_valid():
                # Save changes to `Member` model
                updated_member = update_form.save()

                # Explicitly sync Member fields to User model fields
                user = updated_member.user
                user.first_name = updated_member.first_name
                user.last_name = updated_member.last_name
                user.email = updated_member.email
                user.save()  # Save User model updates
                user_updated = True  # Indicate successful update

            # 2. Update the shipping address
            if shipping_form.is_valid():
                shipping_form.save()
                shipping_updated = True  # Indicate successful update

            # Provide success message depending on the forms updated
            if user_updated or shipping_updated:
                messages.success(request, "Your account has been updated!")


        # Render the form template with a proper context (GET or POST)
        return render(request, "user_auth/update_user.html", {
            "update_form": update_form,
            "shipping_form": shipping_form
        })

    else:
        messages.error(request, "You must be logged in to access this page")
        return redirect("index")





# @login_required (login_url="login") #have to be logged in to view the page
def update_password(request):

    if request.user.is_authenticated:
        current_user = User.objects.get(id = request.user.id)
        if request.method == 'POST':
            #do stuff
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated! Please log in again")
                return redirect("login")
            else:
                messages.success(request, "You have to use matching passwords")
                return redirect("update-password")

        else:
            form= ChangePasswordForm(request.user)
            return render(request, 'user_auth/update_password.html', {'form': form})

    else:
        messages.success(request, "You must be logged in to access this page")
        return redirect('index')


def search(request):
    # determine if they filled out the form
    searched = request.POST['searched']
    #Query database model data
    searched = Product.objects.filter(Q (brand__icontains=searched) | Q (model__icontains=searched) | Q (description__icontains=searched))

    #conditions  for no result
    if not searched:
        messages.success(request, "Please, try your search again")
        return render(request, 'user_auth/index.html', {})

    else:
        return render(request, 'user_auth/search.html', {'searched': searched})



def delete_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_user.delete()
        messages.success(request, "Your account has been deleted!")
        return redirect("index")
