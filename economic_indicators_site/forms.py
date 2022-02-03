from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, HiddenInput
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


class LoginUserForm(AuthenticationForm):
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


class TestRegisterForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'username']


class AddUserCompanyForm(ModelForm):
    class Meta:
        model = models.CompanySystemUser
        fields = ['user', 'company']
        # widgets = {
        #     'user': HiddenInput()
        # }
