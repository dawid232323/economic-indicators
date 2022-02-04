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


class AddNewAssetsForm(ModelForm):
    def save(self, commit=True):
        if commit:
            user = self.cleaned_data.get('user')
            time = self.cleaned_data.get('time_period')
            self.instance.save(user=user, time_period=time)
            return self.instance

    class Meta:
        model = models.Assets
        exclude = ['created_by', 'time_period', 'identifier', 'tangible_fixed_assets',
                   'all_fixed_assets', 'sum_of_supplies', 'sum_of_debts', 'sum_of_current_assets']


class AddNewLiabilities(ModelForm):
    def save(self, commit=True):
        if commit:
            user = self.cleaned_data.get('user')
            time = self.cleaned_data.get('time_period')
            self.instance.save(user=user, time_period=time)
            return self.instance

    class Meta:
        model = models.Liabilities
        exclude = ['created_by', 'time_period', 'identifier', 'short_term_liabilities',
                   'sum_liabilities_and_provisions']
