from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomUserCreateForm
from .models import CustomUser


class CustomRegisterView(CreateView):
    """
    Страница регистрации нового пользователя.
    """

    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class CustomLoginView(LoginView):
    """
    Страница для входа пользователя в систему.
    """

    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("catalog:home")


class CustomLogoutView(LogoutView):
    """
    Страница для выхода пользователя из системы.
    """

    template_name = "users/logout.html"
