from django.db.models import Q
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from test_task_app.forms import UrlForm, LoginForm, RegisterForm, GetCsvForm, DeleteCsvForm
import csv
import requests

from test_task_app.models import CSVFiles, CSVData


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
            try:
                download = s.get(url)
            except:
                return render(request, "download_error.html")
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            data_list = list(cr)

            # fixme: CSVFiles.objects.all().delete()

            if CSVFiles.objects.filter(Q(file_name=name) | Q(file_url=url)).exists():
                return render(request, "already_exist.html")

            csv_file = CSVFiles.objects.create(file_name=name, file_url=url, file_column_name=" , ".join(data_list[0]))
            for i, column in enumerate(data_list[1:]):
                CSVData.objects.create(column_id=csv_file, column_data=" , ".join(column), id=i + 1)

            # split_column_name = column_names.split(",")

            return render(request, "successful_download.html")


class GetCsvView(View):
    @staticmethod
    def get(request):
        get_csv_form = GetCsvForm()
        return render(request, "get_csv_file.html", {"form": get_csv_form})

    # todo: заменить column_id на csv_file id
    # todo: сделать сортировку полей !!!
    @staticmethod
    def post(request):
        csv_file_name: str = request.POST.get("file_name", None)

        try:
            current_file = CSVFiles.objects.get(file_name=csv_file_name)
            current_file_data = CSVData.objects.filter(column_id=current_file)
        except:
            return render(request, "file_not_found.html")

        for i in current_file_data:
            print(i.column_data)

        return render(request, "csv_file_data.html", {"file_info": current_file,
                                                      "file_data": current_file_data})


class DeleteCsvView(View):
    @staticmethod
    def get(reqeust):
        delete_csv_form = DeleteCsvForm()
        return render(reqeust, "delete_csv_file.html", {"form": delete_csv_form})

    @staticmethod
    def post(request):
        csv_file_name: str = request.POST.get("file_name", None)

        try:
            current_file = CSVFiles.objects.get(file_name=csv_file_name).delete()
            CSVData.objects.filter(column_id=current_file).delete()
            return render(request, "successful_delete.html")
        except:
            return render(request, "file_not_found.html")


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
            users = User.objects.get(username=login, password=password)
            print(users.username, users.email, users.email)
        except User.DoesNotExist:
            return render(request, "authorization_fail.html")
        return HttpResponseRedirect("/index")


class RegisterView(View):
    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, "register.html", {"form": register_form})

    @staticmethod
    def post(request):
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)

        # todo:решить проблему с повторяющимися паролями
        again_password = request.POST.get("again_password", None)
        email = request.POST.get("email", None)
        if password != again_password:
            return HttpResponse("<h1>Пароли не совпадают<h1>")
        if User.objects.filter(Q(username=login) | Q(email=email)).exists():
            return render(request, "registration_fail.html")
        User.objects.create(username=login, password=password, email=email)
        return HttpResponseRedirect('/login')


def main_page(request):
    return render(request, "main_page.html")
