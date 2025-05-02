from django.shortcuts import render, redirect, get_object_or_404
from .form import AddProduct, AddProductTest
from .models import Product, Category
from django.http import Http404,HttpResponse

from django.contrib import messages

# Custom 404 error handler
def custom_404_view(request, exception):
    return render(request, "product/404.html", status=404)



def add_product(request):
    if request.method == 'POST':
        # Handle the form submission here (e.g., save input data, process logic)
            form = AddProduct(request.POST, request.FILES)
            if form.is_valid():
                form.save()  # validating the values of inputs
                return redirect("add-product") #after processing redirect to
    else:
        form = AddProduct()

    context = {'productform': form}  # Return the generated description (if any)


    return render(request, 'product/add_product.html', context)

def test_add_product(request):
    if request.method == 'POST':
        # Handle the form submission here (e.g., save input data, process logic)
            form = AddProductTest(request.POST, request.FILES)
            if form.is_valid():
                form.save()  # validating the values of inputs
                messages.success(request, "Your product has been added successfully!")
                return redirect("add-product-test") #after processing redirect to

    else:
        form = AddProductTest()

    context = {'productformtest': form}  # Return the generated description (if any)


    return render(request, 'product/test_add_product.html', context)


def show_products(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request,'product/show_products.html', context)


def category_rods(request, category_id):

    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    context = {'category': category, 'products': products}
    return render(request, 'product/category_search.html', context)



def product_details(request, id):
    product = Product.objects.get(id=id) #getting just one product not list of products
    context = {'product': product}
    return render(request, 'product/product_details.html', context)


def delete_product(request, id):
    pass


def category_summary(request):
    #get all categories from db
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'product/category_summary.html', context)


