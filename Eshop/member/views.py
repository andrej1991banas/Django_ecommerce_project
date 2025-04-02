from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
from product.models import Product, Category
from django.contrib import messages





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

    context= {'registerform':form}

    return render(request, 'user_auth/register.html', context=context)



@login_required (login_url="login") #have to be logged in to view the page
def dashboard(request):
    current_user = request.user
    current_member = current_user.member
    orders = current_member.orders.all()  # Fetch all orders for this member

    context = {
        'username': current_user.username,  # Username
        'email': current_user.email,  # Email
        'first_name': current_user.first_name,  # First Name
        'last_name': current_user.last_name,  # Last Name
        'location': current_member.location,  # Member's location
        'phone': current_member.phone_number,
        'orders': orders,
    }
    return render(request, 'user_auth/dashboard.html', context)



def logout(request):
    auth.logout(request) #creating request for HTML file to apply logout
    messages.success(request, f"You logged out successfully!")
    return redirect("")

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