from django.urls import path

from .views import CustomLoginView, CustomLogoutView, CustomRegisterView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("profile/", ProfileUpdateView.as_view(), name="profile")
]
