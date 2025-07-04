from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Post


class PostListView(ListView):
    """
    Выводит список постов.
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """
        Возвращает только опубликованные записи, отсортированные по дате создания.
        """
        return Post.objects.filter(is_published=True).order_by("-created_at")


class PostDetailView(DetailView):
    """
    Выводит информацию о посте.
    Увеличивает счётчик просмотров при каждом открытии.
    """

    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """
        Получает объект поста и увеличивает его счётчик просмотров.
        """
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj


class PostCreateView(CreateView):
    """
    Создание новой записи блога.
    """

    model = Post
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("post_list")


class PostUpdateView(UpdateView):
    """
    Редактирование существующей записи блога.
    """

    model = Post
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blog/post_form.html"

    def get_success_url(self):
        """
        Перенаправление на страницу просмотра отредактированной статьи.
        """
        return self.object.get_absolute_url()


class PostDeleteView(DeleteView):
    """
    Удаление записи блога с подтверждением.
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")
