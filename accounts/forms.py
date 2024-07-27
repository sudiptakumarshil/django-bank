from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import UserAddress, UserBankAccount
from .constants import *
from django import forms
import random


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER)
    street = forms.Textarea()
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=80)
    type = forms.ChoiceField(choices=ACCOUNT_TYPE)

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
            "type",
            "birth_date",
            "gender",
            "postal_code",
            "country",
            "city",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            gender = self.cleaned_data["gender"]
            postal_code = self.cleaned_data["postal_code"]
            country = self.cleaned_data["country"]
            city = self.cleaned_data["city"]
            type = self.cleaned_data["type"]
            birth_date = self.cleaned_data["birth_date"]

            UserAddress.objects.create(
                user=user,
                postal_code=postal_code,
                country=country,
                city=city,
            )

            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                type=type,
                birth_date=birth_date,
                account_no=10000 + random.randint(0, 9) + user.id,
            )
        return user


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    gender = forms.ChoiceField(choices=GENDER)
    # street = forms.Textarea()
    city = forms.CharField(max_length=50)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=80)
    type = forms.ChoiceField(choices=ACCOUNT_TYPE)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_account = self.instance.Account
                user_address = self.instance.Address
            except UserBankAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields["type"].initial = user_account.type
                self.fields["gender"].initial = user_account.gender
                self.fields["birth_date"].initial = user_account.birth_date
                # self.fields["street"].initial = user_address.street
                self.fields["city"].initial = user_address.city
                self.fields["postal_code"].initial = user_address.postal_code
                self.fields["country"].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserBankAccount.objects.get_or_create(user=user)
            user_address, created = UserAddress.objects.get_or_create(user=user)

            user_account.type = self.cleaned_data["type"]
            user_account.gender = self.cleaned_data["gender"]
            user_account.birth_date = self.cleaned_data["birth_date"]
            user_account.save()

            # user_address.street = self.cleaned_data["street"]
            user_address.city = self.cleaned_data["city"]
            user_address.postal_code = self.cleaned_data["postal_code"]
            user_address.country = self.cleaned_data["country"]
            user_address.save()

        return user
