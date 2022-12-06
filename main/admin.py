from django.contrib import admin

from .models import Shoe, OrderShoe, Order


admin.site.register(Shoe)
admin.site.register(OrderShoe)
admin.site.register(Order)