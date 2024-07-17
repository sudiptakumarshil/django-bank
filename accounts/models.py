from django.db import models
from django.contrib.auth.models import User
from .constants import *


# Create your models here.
class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='Account', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=50, choices=GENDER)
    initial_deposite_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)


class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='Address', on_delete=models.CASCADE)
    street = models.TextField()
    city = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=80)
