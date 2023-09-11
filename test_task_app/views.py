from django.http import HttpResponse
from django.views import View
#import csv


class CsvView(View):
    @staticmethod
    def get(request):
        url = request.GET.get("url", None)
        return HttpResponse(f"<h1>Привет {url}<h1>")

