from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="accounts.register"),
    path("login/", UserLoginView.as_view(), name="accounts.login"),
    path("logout/", UserLogoutView.as_view(), name="accounts.logout"),
    path("profile/", UserBankAccountUpdateView.as_view(), name="accounts.profile"),
]
