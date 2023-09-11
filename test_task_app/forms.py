from django.forms import Form
from django.forms import fields

class UrlForm(Form):
    url = fields.URLField(label="dataset url",
                          help_text="Введите url-адрес необходимого csv-файла",
                          required=True)
