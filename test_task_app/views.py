from django.db.models import Q
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.views import View
from test_task_app.forms import UrlForm, LoginForm, RegisterForm
import csv
import requests

from test_task_app.models import User, CSVFiles, CSVColumns


class CsvView(View):
    @staticmethod
    def get(request):
        url_form = UrlForm()
        return render(request, "url_entering.html", context={"form": url_form})

    @staticmethod
    def post(request):
        url: str = request.POST.get("url", None)
        name: str = request.POST.get("name", None)

        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            column_names = ",".join(my_list[0])

            if CSVFiles.objects.filter(Q(file_name=name) | Q(file_url=url)).exists():
                return HttpResponse("<h1>Файл с такими данными уже существует<h1>")

            csv_file = CSVFiles.objects.create(file_name=name, file_url=url)
            CSVColumns.objects.create(file_id=csv_file.id, column_name=column_names)

            split_column_name = column_names.split(",")
            return HttpResponse(f"<h1>{name}<h1>"
                                f"{split_column_name}")


def index(request):
    return render(request, "index.html")


class LoginView(View):
    @staticmethod
    def get(request):
        login_form = LoginForm()
        return render(request, "login.html", {"form": login_form})

    @staticmethod
    def post(request):
        login: str = request.POST.get("login", None)
        password: str = request.POST.get("password", None)

        try:
            users = User.objects.get(login=login, password=password)
            print(users.login, users.email, users.email)
        except User.DoesNotExist:
            return HttpResponse(f"<h1>Авторизация не пройдена <h1>")
        return HttpResponsePermanentRedirect("/index")


class RegisterView(View):
    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, "register.html", {"form": register_form})

    @staticmethod
    def post(request):
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)

        #todo:решить проблему с повторяющимися паролями
        #again_password = request.POST.get("again_password", None)
        email = request.POST.get("email", None)

        if User.objects.filter(Q(login=login) | Q(email=email)).exists():
            return HttpResponse("<h1>Пользователь с такими данными уже зарегистрирован<h1>")
        User.objects.create(login=login, password=password, email=email)
        return HttpResponsePermanentRedirect('/login')
