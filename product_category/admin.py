from django.contrib import admin

# Import a single model
from .models import (Product, Customer, Order, OrderItem, ShippingAddress)

# import all model(s)
# from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)