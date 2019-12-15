from django.contrib import admin
from .models import (Item, OrederItem , Order,
                    Address, Coupon, ClientMessage)


#custom action hy3ml refund request Fales w y5la refund granted True
def make_refund_accepted(ModelAdmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'refund granted successfuly'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered','in_way',
                    'received', 'refund_requested', 'refund_granted',
                    'billing_address','shipping_address','payment', 'coupon']

    list_display_links = ['user', 'billing_address','shipping_address','payment', 'coupon',]

    list_filter = ['ordered','in_way',
                     'received', 'refund_requested', 'refund_granted',]

    search_fields= ['coupon__code', 'user__username','refrance_code']


    actions = [make_refund_accepted]


admin.site.register(Item)
admin.site.register(OrederItem )
admin.site.register(Order, OrderAdmin)

admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(ClientMessage)
