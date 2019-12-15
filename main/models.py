from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings
from django_countries.fields import CountryField

User = settings.AUTH_USER_MODEL

FOR_WHO_CHOISE= (
('M','men'),
('W', 'women'),
('A', 'accessories')
)

CATEGORY_CHOISE= (
('S','shirt'),
('D','dress'),
('J','Jacket'),
('T','trouser'),
('B','boot'),
('A', 'accessoriess'),
)

QUALITY_CHOISE = (
('YES', 'YES'),
('No', 'NO'),
)

ADDRESS_CHOICE = (
('S', 'shipping'),
('B', 'billing'),
)



class Item(models.Model):
    title = models.CharField(max_length = 23)
    new_price = models.FloatField()
    old_price = models.FloatField(blank=True, null=True)
    image = models.ImageField()
    description = models.TextField()
    for_who = models.CharField(max_length = 1, choices= FOR_WHO_CHOISE)
    category = models.CharField(max_length = 1, choices= CATEGORY_CHOISE)
    stock = models.IntegerField()
    new_arrival = models.BooleanField()

    size = models.CharField(max_length = 23,)
    width = models.FloatField()
    height = models.FloatField()
    weight = models.IntegerField()
    quality_checking = models.CharField(max_length = 3, choices= QUALITY_CHOISE )

    code = models.CharField(max_length = 23, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(default = timezone.now)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('main:item_detail', kwargs={'slug':self.slug})



class OrederItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    quantity  = models.IntegerField(default=1)
    ordered   = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


    def get_total_price(self):
        return self.quantity * self.item.new_price

    def get_total_discount(self):
        if self.item.old_price:
            return self.quantity * (self.item.old_price - self.item.new_price)
        else:
            return 0


"""
1- add item to cart
2- adding billing adress
3- payment
4- being delivered
5- received
6- refunds
"""
class Order(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrederItem )

    ref_code = models.CharField(max_length=20)
    ordered  = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(default = timezone.now)

    shipping_address = models.ForeignKey('Address', related_name="shipping_address",
                                        on_delete=models.SET_NULL, blank=True, null=True)
    billing_address  = models.ForeignKey('Address', related_name="billing_address",
                                        on_delete=models.SET_NULL, blank=True, null=True)

    payment          = models.ForeignKey('Payment',on_delete=models.SET_NULL,
                                        blank=True, null=True)

    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, blank=True, null=True)


    in_way   = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted   = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    def get_Subtotal(self):
        total = 0
        for item_order in self.items.all():
            total += item_order.get_total_price()
        return total

    def get_subtotal_discount(self):
        total = 0
        for item_order in self.items.all():
            total += item_order.get_total_discount()
        return total

    def get_total(self):
        total = 0
        for item_order in self.items.all():
            total += item_order.get_total_price()

        if self.coupon:
            total -= self.coupon.amount

        return total


class Payment(models.Model):
    stripe_charges_id = models.CharField(max_length= 50)
    user              = models.ForeignKey(User, on_delete=models.SET_NULL,
                        blank=True, null=True)
    amount            = models.FloatField()
    timetemp          = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


class Refund(models.Model):
    order     =  models.ForeignKey(Order, on_delete=models.CASCADE)
    email    = models.EmailField()
    reason   = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.order.ref_code}"



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_one  = models.CharField(max_length=325)
    address_two  = models.CharField(max_length=325)
    phone_number = models.IntegerField(blank=True, null=True)
    email   = models.EmailField(blank=True, null=True)
    country = CountryField(multiple=False)
    zip     = models.CharField(max_length=9)
    town    = models.CharField(max_length=325)
    address_type = models.CharField(max_length=1, choices= ADDRESS_CHOICE)
    defualt = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Coupon(models.Model):
    code = models.CharField(max_length=16)
    amount = models.IntegerField()

    def __str__(self):
        return self.code



class ClientMessage(models.Model):
    message= models.TextField()
    name = models.CharField(max_length=75)
    email = models.EmailField()
    subject = models.CharField(max_length= 235)
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.name
