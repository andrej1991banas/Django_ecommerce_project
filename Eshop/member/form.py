from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from .models import Member
from django.db import transaction

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].label = ''
        self.fields[
            'new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields[
            'new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'



class UpdateUserForm(UserChangeForm):
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}), required=False)
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=False)
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=False)
    phone_number = forms.CharField(label="", max_length=20,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Phone Number'}), required=False)
    address1 = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}), required=False)
    address2 = forms.CharField(label="", max_length=100,
                                       widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}), required=False)
    city = forms.CharField(label="", max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
    state = forms.CharField(label="", max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    zipcode = forms.CharField(label="", max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}), required=False)
    country = forms.CharField(label="", max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)

    password = None
    class Meta:
        model = Member
        fields = ['first_name', 'last_name','email', 'phone_number', 'address1', 'address2', 'city', 'state', 'zipcode', 'country']



#create and register the user
class CreateUserForm(UserCreationForm):
    # Additional fields
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    # address1 = forms.CharField(label="", max_length=100,
    #                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}))
    # address2 = forms.CharField(label="", max_length=100,
    #                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}))
    # city = forms.CharField(label="", max_length=100,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
    # state = forms.CharField(label="", max_length=100,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}))
    # zipcode = forms.CharField(label="", max_length=100,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}))
    # country = forms.CharField(label="", max_length=100,
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def save(self, commit=True):
        with transaction.atomic(): #making sure will commit all or nothing
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name'].capitalize()
            user.last_name = self.cleaned_data['last_name'].capitalize()
            if commit:
                user.save()

            # Create the related Member instance
            Member.objects.create(
                user=user,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                phone_number=self.cleaned_data.get('phone_number', ''),

            )

        return user


#authenticate the user (Model form)
class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=TextInput())
    password= forms.CharField(widget=PasswordInput())

