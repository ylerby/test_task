from typing import Iterable
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from test_task_app.forms import UrlForm, LoginForm, RegisterForm, GetCsvForm, DeleteCsvForm, FileSortingForm
from test_task_app.models import CSVFiles, ColumnData
import csv
import requests


class CsvView(View):
    """Класс-представление для скачивания csv-файла"""

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

            if CSVFiles.objects.filter(Q(file_name=name) | Q(file_url=url)).exists():
                return render(request, "already_exist.html")

            csv_file = CSVFiles.objects.create(file_name=name, file_url=url)

            for i, column in enumerate(data_list):
                for j in range(len(data_list[0])):
                    if len(column) == len(data_list[0]):
                        ColumnData.objects.create(col_id=j, raw_id=i, data=column[j], file_id_id=csv_file.id)
            return render(request, "successful_download.html")


class GetCsvView(View):
    """Класс-представление для получения csv-файла"""

    @staticmethod
    def get(request):
        get_csv_form = GetCsvForm()
        return render(request, "get_csv_file.html", {"form": get_csv_form})

    @staticmethod
    def post(request):
        csv_file_name: str = request.POST.get("file_name", None)

        try:
            current_file = CSVFiles.objects.get(file_name=csv_file_name)
            current_file_data = ColumnData.objects.filter(file_id_id=current_file)
        except:
            return render(request, "file_not_found.html")

        length: int = get_line_length(current_file_data)

        full_data = get_full_data(length, current_file_data)

        return render(request, "csv_file_data.html", {"file_info": current_file,
                                                      "file_data": full_data})


class DeleteCsvView(View):
    """Класс-представление для удаления csv-файла"""

    @staticmethod
    def get(reqeust):
        delete_csv_form = DeleteCsvForm()
        return render(reqeust, "delete_csv_file.html", {"form": delete_csv_form})

    @staticmethod
    def post(request):
        csv_file_name: str = request.POST.get("file_name", None)

        try:
            current_file = CSVFiles.objects.get(file_name=csv_file_name).delete()
            ColumnData.objects.filter(file_id_id=current_file).delete()
            return render(request, "successful_delete.html")
        except:
            return render(request, "file_not_found.html")


def index(request) -> HttpResponse:
    return render(request, "index.html")


class LoginView(View):
    """Класс-представление для авторизации"""

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
    """Класс-представление для регистрации"""

    @staticmethod
    def get(request):
        register_form = RegisterForm()
        return render(request, "register.html", {"form": register_form})

    @staticmethod
    def post(request):
        login = request.POST.get("login", None)
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)

        if User.objects.filter(Q(username=login) | Q(email=email)).exists():
            return render(request, "registration_fail.html")
        User.objects.create(username=login, password=password, email=email)
        return HttpResponseRedirect('/login')


class FileSorting(View):
    """Класс-представление для """

    @staticmethod
    def get(request) -> HttpResponse:
        file_sorting_form = FileSortingForm()

        current_file_name = request.GET.get("file_name")
        current_file = CSVFiles.objects.get(file_name=current_file_name)
        current_file_data = ColumnData.objects.filter(file_id_id=current_file.id)

        length = get_line_length(current_file_data)

        return render(request, "file_sorting.html", {"form": file_sorting_form,
                                                     "number_of_columns": length})

    @staticmethod
    def post(request):
        column_id = int(request.POST.get("column_id", None))
        current_file_name = request.GET.get("file_name")

        current_file = CSVFiles.objects.get(file_name=current_file_name)
        current_file_data = ColumnData.objects.filter(file_id_id=current_file.id)

        length = get_line_length(current_file_data)

        full_data = get_full_data(length, current_file_data)

        sorted_data_list = list(sorted(full_data, key=lambda x: x.split(",")[column_id]))
        return render(request, "sorted_csv_file.html", {"data": sorted_data_list})


def main_page(request) -> HttpResponse:
    """Представление для главной страницы"""

    return render(request, "main_page.html")


def get_line_length(data: Iterable) -> int:
    """Получение длины кортежа"""

    length: int = 0
    for column in data:
        if int(column.col_id) > length:
            length = int(column.col_id)
    return length


def get_full_data(length: int, current_file_data: Iterable) -> list:
    """Получение списка со всеми данными из csv файла"""

    full_data = []
    data = []

    for column in current_file_data:
        data.append(column.data)
        if column.col_id == length:
            full_data.append(", ".join(data))
            data = []
            continue

    return full_data


def get_all_files(request):
    """Получение списка со всеми данными из csv файла"""

    data = ColumnData.objects.all()
    file_set: set = set()

    for column in data:
        file_set.add(column.file_id_id)

    separated_data = {file_number: [column.data for column in data if file_number == column.file_id_id] for
                      file_number in file_set}

    return render(request, "all_files_data.html", {"data": separated_data})
