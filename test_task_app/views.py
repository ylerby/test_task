from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from test_task_app.forms import UrlForm
import pandas
import csv
import requests


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