from django.shortcuts import render, redirect, get_object_or_404
from .form import AddProduct
from .models import Product
from django.http import HttpResponse
from .utils import generate_product_description


def add_product(request):
    if request.method == 'POST':
        # Handle the form submission here (e.g., save input data, process logic)
            form = AddProduct(request.POST)
            if form.is_valid():
                form.save()  # validating the values of inputs
                return redirect("add-product") #after processing redirect to
    else:
        form = AddProduct()

        context = {'productform': form}  # Return the generated description (if any)


    return render(request, 'product/add_product.html', context)



def your_name(request):
    return render(request,'product/your_name.html')



def show_products(request):
    products = Product.objects.all()
    context = {'products': products}

    return render(request,'product/show_products.html', context)


#
# def generate_product_description_view(request, product_id):
#     # View to generate a product description for a specific product.
#     if request.method == "POST":
#         product = get_object_or_404(Product, id=product_id)
#
#         # Assume the prompt is submitted through a form
#         prompt = request.POST.get("prompt")
#         if not prompt:
#             return HttpResponse("Prompt is required!", status=400)
#
#         # Generate the description using the utility
#         description = generate_product_description(prompt)
#
#         if description:
#             product.description = description
#             product.save()
#             return HttpResponse("Product description updated successfully!")
#         else:
#             return HttpResponse("Failed to generate description!", status=500)
#     else:
#         return render(request, "generate_description.html")


def product_details(request, id):
    product = Product.objects.get(id=id) #getting just one product not list of products
    context = {'product': product}
    return render(request, 'product/product_details.html', context)

def delete_product(request, id):
    pass
