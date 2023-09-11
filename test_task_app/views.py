from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from test_task_app.forms import UrlForm, LoginForm, RegisterForm
from django.http.response import HttpResponseNotAllowed
import csv
import requests

from test_task_app.models import User


class CsvView(View):
    @staticmethod
    def get(request):
        url_form = UrlForm()
        return render(request, "url_entering.html", context={"form": url_form})

    @staticmethod
    def post(request):
        url = request.POST.get("url", None)
        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            return HttpResponse(f"{my_list[0]}")


def index(request):
    return render(request, "index.html")


def login(request):
    login_form = LoginForm()
    return render(request, "login.html", {"form": login_form})


class RegisterView(View):
    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, "register.html", {"form": register_form})

    @staticmethod
    def post(request):
        login: str = request.POST.get("login", None)
        password: str = request.POST.get("password", None)
        again_password: str = request.POST.get("again_password", None)
        email: str = request.POST.get("email", None)

        #todo: сделать проверку на повторяющийся пароль, сделать проверку на наличие почты, пароля, логина в бд
        #todo: сделать страницу ошибки, в случае невалидных данных
        if (len(list(filter(lambda x: x is not None, [login, password, again_password, email])))
                == len([login, password, again_password, email])):
            if password == again_password:
                User.objects.create(login=login, password=password, email=email)
            else:
                raise HttpResponseNotAllowed
        return HttpResponse("<h1>Создан пользователь<h1>")
