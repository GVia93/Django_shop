from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomUserCreateForm
from .models import CustomUser


class CustomRegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = "users:register"
    success_url = reverse_lazy("catalog:home")


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("catalog:home")


class CustomLogoutView(LogoutView):

    next_page = reverse_lazy("users:login")
