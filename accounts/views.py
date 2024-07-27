from django.views.generic import FormView
from django.contrib.auth import login, logout
from accounts.forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View


class UserRegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("accounts.register")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "User Registration"
        return context


class UserLoginView(LoginView):
    template_name = "accounts/register.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["heading"] = "User Login"
        return context


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy("home")


class UserBankAccountUpdateView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        context = {}
        context["form"] = UserUpdateForm(instance=request.user)
        context["heading"] = "User Profile"
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts.profile")
        return render(request, self.template_name, {"form": form})
