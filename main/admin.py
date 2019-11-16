from django.contrib import admin
from .models import Item, OrederItem , Order, Address, Coupon


admin.site.register(Item)
admin.site.register(OrederItem )
admin.site.register(Order)

admin.site.register(Address)
admin.site.register(Coupon)
