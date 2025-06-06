from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Главная страница")


def contacts(request):
    return HttpResponse("Контакты")
