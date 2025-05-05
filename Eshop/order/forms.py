from django import forms
from .models import ShippingAddress



class ShippingAddressForm(forms.ModelForm):
    shipping_first_name = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}), required = True)
    shipping_last_name = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=True)
    shipping_email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}), required = True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address 1'}), required = True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Address 2'}), required = False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City'}), required = True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'State'}), required = False)
    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Zip Code'}), required = True)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Shipping country'}), required = True)


    class Meta:
        model = ShippingAddress
        fields = ['shipping_first_name', 'shipping_last_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']

        exclude = ['shipping_user',]

    def save(self, commit=True):
        # Call the parent save method but don't immediately commit to the database
        shipping_address = super().save(commit=False)

        # Add any required custom behavior (like cleaning or additional logic)
        shipping_address.shipping_first_name = self.cleaned_data['shipping_first_name']
        shipping_address.shipping_last_name = self.cleaned_data['shipping_last_name']
        shipping_address.shipping_email = self.cleaned_data['shipping_email']
        shipping_address.shipping_address1 = self.cleaned_data['shipping_address1']
        shipping_address.shipping_address2 = self.cleaned_data.get('shipping_address2', '')  # Optional
        shipping_address.shipping_city = self.cleaned_data['shipping_city']
        shipping_address.shipping_state = self.cleaned_data.get('shipping_state', '')  # Optional
        shipping_address.shipping_zipcode = self.cleaned_data['shipping_zipcode']
        shipping_address.shipping_country = self.cleaned_data['shipping_country']

        if commit:
            shipping_address.save()

        return shipping_address


class PaymentForm(forms.Form):
    #we are not savinig this data into database
    card_name = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name On Card'}), required = True)
    card_number = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Card Number'}), required = True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Card Exp Date'}), required = True)
    card_cvv_number = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'CVV Number'}), required = True)
    card_address1 = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Billing Address'}), required = True)
    card_address2  = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Billing Address'}), required = False)
    card_city = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Billing City'}), required = True)
    card_state = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Billing State'}), required = False)
    card_zipcode =  forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Billing Zipcode'}), required = True)
    card_country = forms.CharField(label="", widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Billing Country'}), required = True)