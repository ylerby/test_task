from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(label="dataset url",
                         help_text="Введите url-адрес необходимого csv-файла",
                         required=True)
    name = forms.CharField(label="Название файла",
                           help_text="Введите название файла, для дальнейшего поиска",
                           required=True)


#todo: сделать валидацию всех полей в соответствии с бд
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
    password_again = forms.CharField(label="Повторение пароля",
                                     help_text="Повторите пароль",
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
