from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# from .models import Product
# import all model(s)
from .models import *
from . utils import *

# Create your views here.
@login_required(login_url='accounts:login')
def basePage(request):
  context = {}
  return render(request, 'product_category/base.html', context)

# Homepage view
@login_required(login_url='accounts:login')
def homePage(request):
  sendFormMessage(request)
  # if request.method == 'POST':
  #   message = request.POST['message']
  #   sender_Email = request.POST['email']
  #   sender_Name = request.POST['sender_name']

  #   send_mail(
  #     subject='Contact Form Message',
  #     message="{}. Sender of this message is {} with an email of {}".format(message, sender_Name, sender_Email),
  #     # from_email = sender_Email,
  #     # recipient_list = [settings.EMAIL_HOST_USER],
  #     from_email = 'ayodelemee@gmail.com',
  #     recipient_list = ['mail4ayodele@gmail.com'],
  #     fail_silently=False
  #     )

  data = cartData(request)
  cartItems = data['cartItems']

  context = {'cartItems': cartItems}
  return render(request, 'product_category/home.html', context)

# Jeans view
@login_required(login_url='accounts:login')
def jeansPage(request):
  obj = Product.objects.filter(category='jeans')

  sendFormMessage(request)

  data = cartData(request)
  cartItems = data['cartItems']

  context = {'object': obj, 'cartItems': cartItems}
  return render(request, 'product_category/jeans.html', context)

# Shirts view
@login_required(login_url='accounts:login')
def shirtsPage(request):
  obj = Product.objects.filter(category='shirts')

  sendFormMessage(request)
  
  data = cartData(request)
  cartItems = data['cartItems']

  context = {'object': obj, 'cartItems': cartItems}
  return render(request, 'product_category/shirts.html', context)

# Sweats views
@login_required(login_url='accounts:login')
def sweatsPage(request):
  queryset = Product.objects.filter(category='sweats')

  sendFormMessage(request)
  
  data = cartData(request)
  cartItems = data['cartItems']

  context = {'object_list': queryset, 'cartItems': cartItems}
  return render(request, 'product_category/sweats.html', context)

# Coats view
@login_required(login_url='accounts:login')
def coatsPage(request):
  obj = Product.objects.filter(category='coats')

  sendFormMessage(request)
  
  data = cartData(request)
  cartItems = data['cartItems']

  context = {'object': obj, 'cartItems': cartItems}
  return render(request, 'product_category/coats.html', context)

# Productdetail view
@login_required(login_url='accounts:login')
def product_details(request, id):
  obj = Product.objects.get(id=id)

  sendFormMessage(request)
  
  data = cartData(request)
  cartItems = data['cartItems']

  context = {'object': obj, 'cartItems': cartItems}
  return render(request, 'product_category/product_details.html', context)

# Cartpage view
@login_required(login_url='accounts:login')
def cartPage(request):
  data = cartData(request)
  items = data['items']
  order = data['order']
  cartItems = data['cartItems']

  sendFormMessage(request)
  
  context = {'items': items, 'order': order, 'cartItems': cartItems}
  return render(request, 'product_category/cart.html', context)

# Checkoutpage view
@login_required(login_url='accounts:login')
def checkoutPage(request):
  data = cartData(request)
  items = data['items']
  order = data['order']
  cartItems = data['cartItems']

  sendFormMessage(request)
  
  context = {'items': items, 'order': order, 'cartItems': cartItems}
  return render(request, 'product_category/checkout.html', context)

# For rendering a HTTP response
def updateItem(request):
  data = json.loads(request.body) # from the body attribute specified in myscrip.js
  productID = data['productID']
  action = data['action']

  print('Action:', action)
  print('ProductID:', productID)

  # to avoid the problem with RelatedObjectDoesNotExist exception
  try:
    customer = request.user.customer
  except Customer.DoesNotExist:
    customer = Customer.objects.create(user=request.user, name=request.user)

  customer = request.user.customer
  product = Product.objects.get(id=productID)
  print("Name of product is: ", product.name)
  print("Price of product is: ", product.price)
  order, created = Order.objects.get_or_create(customer=customer, complete=False)
  orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

  print("Order quantity before is: ", orderItem.quantity)

  if action == 'add':
    orderItem.quantity = (orderItem.quantity + 1)
  elif action == 'remove':
    orderItem.quantity = (orderItem.quantity - 1)

  orderItem.save()
  print("Order quantity after is: ", orderItem.quantity)

  if orderItem.quantity <= 0:
    orderItem.delete()
  return JsonResponse('Item was added', safe=False)

# request for processOrder is the response.json() returned by the first promise in the javascript within the checkout.html file
def processOrder(request):
  print('Data:', request.body)
  transaction_id = datetime.datetime.now().timestamp()
  data = json.loads(request.body)

  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

  else:
    customer, order = guestOrder(request, data)

  total = float(data['form']['total'])
  order.transaction_id = transaction_id

  # verifying if the front end total is the same as value on the backend
  # to prevent theft 
  if total == float(order.get_cart_total):
    order.complete = True
  order.save()

  if order.shipping == True:
    ShippingAddress.objects.create(
      customer=customer,
      order=order,
      address=data['shipping']['address'],
      city=data['shipping']['city'],
      state=data['shipping']['state'],
      zipcode=data['shipping']['zipcode'],
    )
  return JsonResponse('Payment completed', safe=False)