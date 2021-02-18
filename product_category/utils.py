import json
from . models import *

from django.core.mail import send_mail
from django.conf import settings

def cookieCart(request):
  try:
    cart = json.loads(request.COOKIES['cart']) # turns our data from json into a python dictionary
  except:
    cart = {}

  items = [] 
  order = {'get_cart_total': 0, 'get_cart_items':0, 'shipping':True}
  cartItems = order['get_cart_items']

  # productID is the key in cart dictionary
  for productID in cart:
    # try except clause incase a product is deleted from our database
    try:
      cartItems += cart[productID]['quantity']
      product = Product.objects.get(id=productID)
      total = (product.price * cart[productID]['quantity'])

      order['get_cart_total'] += total
      order['get_cart_items'] += cart[productID]['quantity']

      item = {
        'product': {
          'id': product.id,
          'name': product.name,
          'price': product.price,
          'imageURL': product.imageURL,
        },
        'quantity': cart[productID]['quantity'],
        'get_total': total
      }
      items.append(item)
    except:
      pass

  return {'items': items, 'order': order, 'cartItems': cartItems}

def cartData(request):
  if request.user.is_authenticated:
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

  else:
    cookieData = cookieCart(request)
    items = cookieData['items']
    order = cookieData['order']
    cartItems = cookieData['cartItems']

  return {'items': items, 'order': order, 'cartItems': cartItems}

def guestOrder(request, data):

  # print('User is not logged in...')

  print('COOKIES:', request.COOKIES)

  # Grab the name of the guest user from the form
  name = data['form']['name']
  email = data['shipping']['email']
  print('1st stage of email: ', email)

  # Grab the items they ordered from the cookieCart
  cookieData = cookieCart(request)
  items = cookieData['items']

  # Create an entry in our database for this guest A.K.A Customer 
  # in order to associate their ordered items with their name
  # and email. NOTE: This is not a user of our website
  # unless they signup and with their credentials
  customer, created = Customer.objects.get_or_create(
    email=email,
  )
  customer.name = name
  customer.save()

  order = Order.objects.create(
    customer=customer,
    complete=False,
  )

  for item in items:
    product = Product.objects.get(id=item['product']['id'])
    orderItem = OrderItem.objects.create(
      product=product, 
      order=order, 
      quantity=item['quantity'],
      )

  return customer, order


def sendFormMessage(request):
    if request.method == 'POST':
      message = request.POST['message']
      sender_Email = request.POST['email']
      sender_Name = request.POST['sender_name']

      send_mail(
        subject='Contact Form Message',
        message="{}. Sender of this message is {} with an email of {}".format(message, sender_Name, sender_Email),
        # from_email = sender_Email,
        # recipient_list = [settings.EMAIL_HOST_USER],
        from_email = 'ayodelemee@gmail.com',
        recipient_list = ['mail4ayodele@gmail.com'],
        fail_silently=False
        )