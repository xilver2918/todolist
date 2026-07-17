from django.urls import include, path

from . import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),

    # Django 기본 로그인·로그아웃 URL
    path("", include("django.contrib.auth.urls")),
]