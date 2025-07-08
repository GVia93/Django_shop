from django import forms
from django.core.exceptions import ValidationError

from .models import Product

FORBIDDEN_WORDS = {
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
}


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов.

    Выполняет валидацию полей name и description:
    запрещает использование определённых слов из списка FORBIDDEN_WORDS.
    """

    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Добавляет CSS-классы Bootstrap ко всем полям формы.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['name'].widget.attrs['placeholder'] = "Введите название продукта."
        self.fields['description'].widget.attrs['placeholder'] = "Введите описание продукта."
        self.fields['image'].help_text = ("Размер сообщения не должен превышать 5 МБ.\n"
                                                          'Изображение должно быть в формате JPEG или PNG.')

    def clean_name(self):
        """
        Проверяет отсутствие запрещённых слов в поле 'name'.
        """
        name = self.cleaned_data["name"]
        self._check_forbidden_words(name, "названии")
        return name

    def clean_description(self):
        """
        Проверяет отсутствие запрещённых слов в поле 'description'.
        """
        description = self.cleaned_data["description"]
        self._check_forbidden_words(description, "названии")
        return description

    def _check_forbidden_words(self, value: str, field_name: str):
        """
        Проверяет строку на наличие запрещённых слов.
        """
        lowered = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise forms.ValidationError(
                    f"Запрещено использовать слово «{word}» в {field_name}."
                )

    def clean_price(self):
        """
        Проверяет, что цена не отрицательная.
        """
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        """
        Проверяет формат изображения.
        """
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер сообщения не должен превышать 5 МБ.')
            if not image.content_type in ['image/jpeg', 'image/png']:
                raise ValidationError('Изображение должно быть в формате JPEG или PNG.')
