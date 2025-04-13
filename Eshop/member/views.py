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
    context = {'products': products}
    # template = loader.get_template('user_auth/index.html')

    return render(request, 'user_auth/index.html', context)



def login(request):
    form= LoginForm()

    if request.method=='POST':
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
                #convert db string to dict, old_cart (str)
                if saved_cart:
                    #convert to dict with JSON
                    converted_cart = json.loads(saved_cart) #from str to dict

                    #add loaded dict to cart_session
                    cart = Cart(request)
                    for key in converted_cart.keys():
                        cart.db_add(product=Product.objects.get(id=key))

                messages.success(request, "Welcome, you successfully logged in!")
                return redirect("dashboard")

            else:
                return HttpResponse("Invalid username or password")  # Error message for failed login
                # return render(request, 'user_auth/login.html', {'loginform': form})
    context= {'loginform':form}
    return render(request, 'user_auth/login.html', context)



def register(request):
    if request.method=="POST":
        form = CreateUserForm(request.POST)#builtin form for create user
        if form.is_valid():
            form.save() #validating the values of inputs
            messages.success(request, "Your account has been created!")
            return redirect("login")
    else:
        form = CreateUserForm()
        for error in list(form.errors.items()):
            messages.error(request, error[1])
            return redirect("register")

    context= {'registerform':form}

    return render(request, 'user_auth/register.html', context=context)




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
    auth.logout(request) #creating request for HTML file to apply logout
    messages.success(request, f"You logged out successfully!")
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


def test (request):
    #testing page
    categories = Category.objects.all()  # Query all categories
    context = {
        'categories': categories,  # Pass categories to the template
    }

    return render(request, 'user_auth/test.html', context)



def update_user(request):
    # Updating the user profile
    if request.user.is_authenticated:
        # Get the currently logged-in user
        current_user = request.user

        # Get the logged-in user's Member object (via the OneToOne relationship)
        try:
            member = current_user.member  # Access the related Member object

        except Member.DoesNotExist:  # Handle the case where the Member instance doesn't exist
            messages.error(request, "Member profile not found.")
            return redirect("dashboard")

        #get current users shipping info
        shipping_user = ShippingAddress.objects.get(shipping_user=request.user.id)

        # Getting the form instance, pre-filled with user data
        update_form = UpdateUserForm(request.POST or None, instance=member) #getting current info from member to the form

        #get users shipping form
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)
        if update_form.is_valid():
            updated_member = update_form.save()
            # Sync changes back to the `User` model (optional fields like `first_name`, `last_name`, etc.)
            user = updated_member.user

            # Access the related User model
            user.first_name = updated_member.first_name
            user.last_name = updated_member.last_name
            user.email = updated_member.email
            user.save()  # Save updates to the User model
            messages.success(request, "Your account has been updated!")
            return redirect("dashboard")


        elif shipping_form.is_valid():
            shipping_form.save()
            messages.success(request, "Your shipping address has been updated!")
            return redirect("dashboard")

        else:
            # Render the form back with errors if validation fails
            messages.success(request, "Fill up the missing fields...")
            return render(request, "user_auth/update_user.html", {"update_form": update_form})


        return render(request, 'user_auth/update_user.html', {'update_form': update_form, 'shipping_form': shipping_form})
    else:
        messages.success(request, "You must be logged in to access this page")
        return redirect('index')


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
                login(request, current_user)
                return redirect("login")
            else:
                for error in list(form.errors.items()):
                    messages.error(request, error[1])
                    return redirect("update-password")

        else:
            form= ChangePasswordForm(request.user)
            return render(request, 'user_auth/update_password.html', {'form': form})

    else:
        messages.success(request, "You must be logged in to access this page")
        return redirect('index')


def search(request):
    # determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query database model data
        searched = Product.objects.filter(Q (brand__icontains=searched) | Q (model__icontains=searched) | Q (description__icontains=searched))

        #conditions  for no result
        if not searched:
            messages.success(request, "Please, try your search again")
            return render(request, 'user_auth/index.html', {
                'searched': []
            })

        else:
            return render(request, 'user_auth/search.html', {'searched': searched})
    else:
        return render(request, 'user_auth/search.html', {})


