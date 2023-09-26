from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(label="dataset url",
                         help_text="Введите url-адрес необходимого csv-файла",
                         required=True)
    name = forms.CharField(label="Название файла",
                           help_text="Введите название файла, для дальнейшего поиска",
                           required=True)


class LoginForm(forms.Form):
    login = forms.CharField(label="Логин",
                            help_text="Введите логин",
                            required=True)
    password = forms.CharField(label="Пароль",
                               help_text="Введите пароль",
                               required=True,
                               widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    login = forms.CharField(label="Логин",
                            help_text="Введите логин",
                            required=True)
    password = forms.CharField(label="Пароль",
                               help_text="Введите пароль",
                               required=True,
                               widget=forms.PasswordInput)
    email = forms.EmailField(label="Электронная почта",
                             help_text="Введите электронную почту",
                             required=True,
                             )


class DeleteCsvForm(forms.Form):
    file_name = forms.CharField(label="Название файла",
                                help_text="Введите название файла, подлежащего удалению",
                                required=True)


class GetCsvForm(forms.Form):
    file_name = forms.CharField(label="Название файла",
                                help_text="Введите название файла, который необходимо получить",
                                required=True)


class FileSortingForm(forms.Form):
    column_id = forms.IntegerField(label="Номер столбца таблицы",
                                   help_text=f"Введите номер столбца",
                                   required=True,
                                   min_value=0)
