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
