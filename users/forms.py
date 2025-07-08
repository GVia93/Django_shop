from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        """
        Добавляет Bootstrap-классы ко всем полям формы.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "exemple@mail.com"
        self.fields["password1"].widget.attrs["placeholder"] = "Введите пароль"
        self.fields["password2"].widget.attrs["placeholder"] = "Повторите пароль"

    def clean_phone_number(self):
        """
        Проверяет, что номер телефона содержит только цифры, если он указан.
        """
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number


class CustomAuthenticationForm(AuthenticationForm):
    """
    Форма для входа пользователя.
    """

    def __init__(self, *args, **kwargs):
        """
        Добавляет Bootstrap-классы ко всем полям формы.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ProfileUpdateForm(forms.ModelForm):
    """
    Форма редактирования профиля.
    """

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "avatar",
        ]

    def __init__(self, *args, **kwargs):
        """
        Добавляет Bootstrap-классы ко всем полям формы.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "exemple@mail.com"
        self.fields["first_name"].widget.attrs["placeholder"] = "Введите ваше имя."
        self.fields["last_name"].widget.attrs["placeholder"] = "Введите вашу фамилию."
        self.fields["phone_number"].widget.attrs["placeholder"] = "+7 (999) 999-99-99"
        self.fields["country"].widget.attrs["placeholder"] = "Укажите страну"
        self.fields["avatar"].help_text = (
            "Размер изображения не должен превышать 5 МБ.\n"
            "Изображение должно быть в формате JPEG или PNG."
        )
