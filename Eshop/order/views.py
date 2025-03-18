# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import Order  # Adjust import based on your structure
#
# @login_required(login_url="login")
# def dashboard(request):
#     current_user = request.user
#     current_member = current_user.member
#     orders = current_member.orders.all()
#
#     # Add total price to each order
#     orders_with_totals = [
#         {
#             'order': order,
#             'total_price': sum(product.price for product in order.products.all())
#         }
#         for order in orders
#     ]
#
#     context = {
#         'username': current_user.username,
#         'email': current_user.email,
#         'first_name': current_user.first_name,
#         'last_name': current_user.last_name,
#         'location': current_member.location,
#         'phone': current_member.phone_number,
#         'orders': orders_with_totals,  # Pass orders with totals
#     }
#     return render(request, 'user_auth/dashboard.html', context)