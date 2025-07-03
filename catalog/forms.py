from django import forms

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
