from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView, View, TemplateView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import (Item,OrederItem ,Order,
                    Address, Coupon,
                    ClientMessage, Payment)
from .forms import (CheckoutForm, CouponForm, ClientMessageForm)

import random
import string
import stripe
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=25))


def is_valid_faild(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid





class HomeView(ListView):
    model = Item
    template_name= 'main/home.html'

    def get_queryset(self):
        return Item.objects.order_by('-update_at')



class ItemListView(ListView):
    model = Item
    paginate_by = 16
    template_name= 'main/category.html'

    def get_queryset(self):
        return Item.objects.order_by('-update_at')



class ItemDetailView(DetailView):
    model = Item
    template_name= 'main/single-product.html'


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user= self.request.user,
                                            ordered=False)

            coupon_form = CouponForm()

            context = {'object':order,
                        'coupon':coupon_form}
            return render(self.request, 'main/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'Sorry you not ordered yet')
            return redirect('main:item_list')


@login_required
def add_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, create = OrederItem.objects.get_or_create(user = request.user,
                                                          item = item,
                                                          ordered=False)

    order_qs = Order.objects.filter(user= request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug= item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, 'Added another item')
            return redirect('main:cart_summry')
        else:
            order.items.add(order_item)
            messages.info(request, 'Added item to cart')

    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")

    return redirect('main:item_detail', slug=slug)



@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrederItem.objects.filter(user = request.user,
                                           item = item,
                                           ordered=False)

    order_qs = Order.objects.filter(user= request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug= item.slug).exists():
            order_item = order_item[0]
            if order_item.quantity > 1:
                order_item.quantity -=1
                order_item.save()
                messages.info(request, 'removed 1 item')

            else:
                order.items.remove(order_item)
        else:
            messages.info(request, 'you not have this item')
            return redirect('main:item_detail', slug=slug)


    else:
        messages.info(request, 'you not have an active order')
        return redirect('main:item_list')

    return redirect('main:cart_summry')


@login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrederItem.objects.filter(user = request.user,
                                           item = item,
                                           ordered=False)

    order_qs = Order.objects.filter(user= request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug= item.slug).exists():
            order_item = order_item[0]
            order.items.remove(order_item)
            messages.info(request, 'removed item')
        else:
            messages.info(request, 'you not have this item')
            return redirect('main:item_detail', slug=slug)
    else:
        messages.info(request, 'you not have an active order')
        return redirect('main:item_list')

    return redirect('main:cart_summry')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
            'form':form,
            'object':order,
            }

            shipping_address_qs = Address.objects.filter(
                                user= self.request.user,
                                address_type = 'S',
                                defualt = True
                                )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address':shipping_address_qs[0]})


            billing_address_qs = Address.objects.filter(
                                user= self.request.user,
                                address_type = 'B',
                                defualt = True
                                )
            if billing_address_qs.exists():
                context.update({'default_billing_address':billing_address_qs[0]})


            return render(self.request, 'main/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'Sorry you not have an active order')
            return redirect('main:home')


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered=False)
            if form.is_valid():

                use_defaulte_shipping = form.cleaned_data.get('use_shipping_address')
                if use_defaulte_shipping:
                    address_qs = Address.objects.filter(user= self.request.user,
                                                        address_type = 'S',
                                                        defualt = True)
                    if address_qs.exists():
                        shipping_adress = address_qs[0]
                        order.shipping_address = shipping_adress
                        order.save()
                    else:
                        messages.info(self.request, 'Sorry you not have a default shipping address')
                        return redirect('main:checkout')

                else:
                    shipping_add1 = form.cleaned_data.get('shipping_address_one')
                    shipping_add2 = form.cleaned_data.get('shipping_address_two')
                    number = form.cleaned_data.get('shipping_phone_number')
                    email = form.cleaned_data.get('shipping_email')
                    shipping_country = form.cleaned_data.get('shipping_country')
                    shiping_zip = form.cleaned_data.get('shipping_zip')
                    shipping_city = form.cleaned_data.get('shipping_town')

                    if is_valid_faild(['shipping_add1', 'number', 'email', 'shiping_zip', 'shipping_city']):
                        shipping_address = Address(
                        user = self.request.user,
                        address_one = shipping_add1,
                        address_two = shipping_add2,
                        phone_number = number,
                        email = email,
                        country = shipping_country,
                        zip = shiping_zip,
                        town = shipping_city,
                        address_type = 'S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_shipping_defualt = form.cleaned_data.get('set_shipping_defualt')
                        if set_shipping_defualt:
                            shipping_address.defualt = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, 'plz fill the required fields')
                        return redirect('main:checkout')


                use_billing_address = form.cleaned_data.get('use_billing_address')
                billing_same_shipping = form.cleaned_data.get('billing_same_shipping')
                if billing_same_shipping:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()


                elif use_billing_address:
                    address_qs = Address.objects.filter(user= self.request.user,
                                                        address_type = 'B',
                                                        defualt = True)
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, 'Sorry you not have a default billing address')
                        return redirect('main:checkout')

                else:
                    billing_add1 = form.cleaned_data.get('billing_address_one')
                    billing_add2 = form.cleaned_data.get('billing_address_two')
                    billing_country = form.cleaned_data.get('billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')
                    billing_city = form.cleaned_data.get('billing_town')

                    if is_valid_faild(['billing_add1','billing_zip', 'billing_city']):
                        billing_address = Address(
                        user = self.request.user,
                        address_one = billing_add1,
                        address_two = billing_add2,
                        country = billing_country,
                        zip = billing_zip,
                        town = billing_city,
                        address_type = 'B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_billing_defualte = form.cleaned_data.get('set_billing_defualte')
                        if set_shipping_defualt:
                            billing_address.defualt = True
                            billing_address.save()
                    else:
                        messages.info(self.request, 'plz fill the required fields')
                        return redirect('main:checkout')

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('main:payment', payment_option='stripe')

                elif payment_option == 'B':
                    return redirect('main:payment', payment_option='paypal')

                else:
                    messages.info(self.request, 'plz select payment Option')
                    return redirect('main:checkout')

            else:
                messages.warning(self.request, 'form not valid ')
                return redirect('main:checkout')

        except ObjectDoesNotExist:
            messages.info(self.request, 'Sorry you not have an active order')
            return redirect('main:home')




class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user = self.request.user, ordered=False)
        return render(self.request, 'main/payment.html')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user= self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        order_amount= int(order.get_total()* 100)

        test_token = stripe.Token.create(card={
        "number": '4242424242424242',
        "exp_month": 12,
        "exp_year": 2056,
        "cvc": '123'})

        try:
            # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
            charge = stripe.Charge.create(
              amount=order_amount,
              currency="usd",
              source=test_token,
            )

            # create the payment
            payment = Payment()
            payment.stripe_charges_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            #assign payment to the order
            order.ordered =True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()

            messages.success(self.request, "Your order was successful!")
            return redirect("/")

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("/payment/stripe/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/payment/stripe/")

        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request, "Invalid parameters")
            return redirect("/payment/stripe/")

        except stripe.error.AuthenticationError as e:
            messages.warning(self.request, "Not authenticated")
            return redirect("/payment/stripe/")

        except stripe.error.APIConnectionError as e:
            messages.warning(self.request, "Network error")
            return redirect("/payment/stripe/")

        except stripe.error.StripeError as e:
            messages.warning(self.request, "Something went wrong. You were not charged. Please try again")
            return redirect("/payment/stripe/")

        except Exception as e:
            messages.warning(self.request, "A serious error occurred. We have been notifed.")
            return redirect("/payment/stripe/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon

    except ObjectDoesNotExist:
        return None




class CouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user= self.request.user, ordered=False)
                coupon = get_coupon(self.request, code)
                if coupon:
                    order.coupon = coupon
                    order.save()
                    messages.info(self.request, 'Added coupon successfuly ')
                    return redirect('main:cart_summry')
                else:
                    messages.info(self.request, 'wrong code try again')
                    return redirect('main:cart_summry')

            except ObjectDoesNotExist:
                messages.info(self.request, 'Sorry you not have an active order')
                return redirect('main:home')







class ClientMessageVeiw(View):
    def get(self, *args, **kwargs):
        return render(self.request,"main/contact.html", )

    def post(self, *args, **kwargs):
        form = ClientMessageForm(self.request.POST or None)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')

            print(message)
            print(name)
            print(email)
            print(subject)

            report = ClientMessage(
                message =message,
                name =name,
                email =email,
                subject =subject,
            )
            report.save()

            messages.success(self.request, 'Thanks For Your message')
            return redirect('main:home')
        else:
            messages.error(self.request, 'sorry some thing wrong! try again')
            return redirect('main:contact')



class ConfirmatonView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user = self.request.user)
            context = { 'order':order,
                        }
            return render(self.request,"confirmation.html",context )

        except ObjectDoesNotExist:
            messages.info(self.request, 'you not have any orders')
            return redirect('main:home')
