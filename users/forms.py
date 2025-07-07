from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.
    """

    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Необязательное поле. Введите ваш номер телефона.",
    )
    country = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "country",
            "phone_number",
            "avatar",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        """
        Проверяет, что номер телефона содержит только цифры, если он указан.
        """
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number

    def __init__(self, *args, **kwargs):
        """
        Добавляет Bootstrap-классы ко всем полям формы.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


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
