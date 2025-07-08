from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import (CustomAuthenticationForm, CustomUserCreateForm,
                    ProfileUpdateForm)
from .models import CustomUser


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования профиля текущего пользователя.
    Доступно только авторизованным пользователям.
    Использует форму ProfileUpdateForm и обновляет модель CustomUser.
    После сохранения перенаправляет на главную страницу.
    """

    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self, queryset=None):
        """
        Возвращает объект текущего пользователя.
        """
        return self.request.user


class CustomRegisterView(CreateView):
    """
    Страница регистрации нового пользователя.
    """

    model = CustomUser
    form_class = CustomUserCreateForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Обрабатывает валидную форму регистрации:
        - сохраняет пользователя,
        - выполняет автоматический вход,
        - отправляет приветственное письмо,
        - возвращает стандартный ответ успешной валидации.
        """
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        """
        Отправляет приветственное электронное письмо новому пользователю.
        """
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


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
