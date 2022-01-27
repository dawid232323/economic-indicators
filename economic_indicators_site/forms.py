from django.forms import ModelForm
from django.forms import PasswordInput

from . import models


class UserRegisterForm(ModelForm):
    class Meta:
        model = models.SystemUser
        fields = ['username', 'password', 'password', 'first_name', 'last_name',
                  'email', 'company']
        labels = {
            'username': 'Nazwa Użytkownika',
            'password': "Hasło",
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'company': 'Firma'
        }
        widgets = {
            'password': PasswordInput()
        }


class LoginUserForm(ModelForm):
    class Meta:
        model = models.SystemUser
        fields = ['username', 'password']
        labels = {
            'username': 'Nazwa Użytkownika',
            'password': 'Hasło'
        }
        widgets = {
            'password': PasswordInput()
        }
