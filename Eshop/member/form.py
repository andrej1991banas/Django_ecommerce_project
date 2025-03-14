from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from .models import Member
from django.db import transaction




#create and register the user
class CreateUserForm(UserCreationForm):
    # Additional fields
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    location = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

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
                first_name=self.cleaned_data['first_name'].capitalize(),
                last_name=self.cleaned_data['last_name'].capitalize(),
                phone_number=self.cleaned_data.get('phone_number', ''),
                location=self.cleaned_data.get('location', '').capitalize(),
            )

        return user


#authenticate the user (Model form)
class LoginForm(AuthenticationForm):
    username= forms.CharField(widget=TextInput())
    password= forms.CharField(widget=PasswordInput())

