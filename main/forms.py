from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICE= (
('S','stripe'),
('p', 'paypal')
)

class CheckoutForm(forms.Form):
    shipping_address_one = forms.CharField(required=False)
    shipping_address_two = forms.CharField(required=False)
    shipping_phone_number = forms.IntegerField()
    shipping_email = forms.EmailField()
    shipping_country = CountryField(blank_label='(select country)').formfield(
                                    required=False,
                                    widget=CountrySelectWidget(attrs={
                                    'class': 'country_select',}))
    shipping_zip = forms.CharField(required=False)
    shipping_town = forms.CharField(required=False)

    billing_address_one = forms.CharField(required=False)
    billing_address_two = forms.CharField(required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
                                    required=False,
                                    widget=CountrySelectWidget(attrs={
                                    'class': 'country_select',}))
    billing_zip = forms.CharField(required=False)
    billing_town = forms.CharField(required=False)

    billing_same_shipping = forms.BooleanField(required=False)
    set_shipping_defualt  = forms.BooleanField(required=False)
    use_shipping_address  = forms.BooleanField(required=False)
    set_billing_defualte  = forms.BooleanField(required=False)
    use_billing_address   = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICE)




class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
                            'class':'form-control',
                            'placeholder':'Do you have coupon? enter the code',
                            'aria-label':"Recipient's username",
                            'aria-describedby':"button-addon2"
    }))
