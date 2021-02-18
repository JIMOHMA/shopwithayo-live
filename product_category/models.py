from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):

  # this is either jeans, shirts, coats or sweats
  category_status = (
    ('coats', 'coats'),
    ('jeans', 'jeans'),
    ('shirts', 'shirts'),
    ('sweats', 'sweats'),
  )

  name = models.CharField(max_length=200)
  price = models.DecimalField(max_digits=9, decimal_places=2)
  image = models.ImageField(null=True, blank=True)
  category = models.CharField(
    max_length=200,
    choices=category_status,
    blank=True,
    default='',
    help_text='Clothing Category',
    )

  def __str__(self):
    return str(self.name)

  #@property decorator allows us to access the url as an attribute instead of a method
  @property
  def imageURL(self):
    try:
      url = self.image.url
    except:
      url = ''
    return url

  def get_absolute_url(self):
    return f"details/{self.id}/"


class Customer(models.Model):
  user = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)

  def __str__(self):
    return str(self.name)



class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
  date_ordered = models.DateTimeField(auto_now_add=True)
  complete = models.BooleanField(default=False, null=True, blank=False)
  transaction_id = models.CharField(max_length=200, null=True)

  def __str__(self):
    return str(self.id)

  # @property
	# def shipping(self):
	# 	shipping = False
	# 	orderitems = self.orderitem_set.all()
	# 	for i in orderitems:
	# 		if i.product.digital == False:
	# 			shipping = True
	# 	return shipping

  @property
  def shipping(Self):
    # This is for digital prodicts
    # shipping = False
    # orderitems = self.order_item_set.all()
    # for i in orderitems:
    #   if i.product.digital == False:
    #     shipping = True

    shipping = True
    return shipping

  # @property
  # def get_cart_total(self):
  #   orderitems = self.orderitem_set.all()
  #   total = sum([item.get_total for item in orderitems])
  #   return total

  @property
  def get_cart_total(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.get_total for item in orderitems])
    return total

  # @property
	# def get_cart_items(self):
	# 	orderitems = self.orderitem_set.all()
	# 	total = sum([item.quantity for item in orderitems])
	# 	return total

  @property
  def get_cart_items(self):
    orderitems = self.orderitem_set.all()
    total = sum([item.quantity for item in orderitems])
    return total

class OrderItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
  quantity = models.IntegerField(default=0, null=True, blank=True)
  date_added = models.DateTimeField(auto_now_add=True) #automaticatically creates a date when an instance of this model is created

  # @property
	# def get_total(self):
	# 	total = self.product.price * self.quantity
	# 	return total

  @property
  def get_total(self):
    total = self.product.price * self.quantity
    return total


class ShippingAddress(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
  order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
  address = models.CharField(max_length=200, null=False)
  city = models.CharField(max_length=200, null=False)
  state = models.CharField(max_length=200, null=False)
  zipcode = models.CharField(max_length=200, null=False)
  date_added = models.DateTimeField(auto_now_add=True) #automaticatically creates a date when an instance of this model is created

  def __str__(self):
    return str(self.address)