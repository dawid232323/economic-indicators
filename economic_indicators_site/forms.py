from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, HiddenInput
from django.forms.widgets import DateInput
from django.forms import PasswordInput

from . import models


class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'password', 'first_name', 'last_name',
                  'email']
        labels = {
            'username': 'Nazwa Użytkownika',
            'password': "Hasło",
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
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
        fields = ['company']

    def save(self, commit=True, **kwargs):
        if commit:
            user = self.cleaned_data.get('user')
            wanted_user = User.objects.get(username=user)
            self.instance.save(user=wanted_user, **kwargs)
            return self.instance


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
        labels = {
            'intangible_fixed_assets': 'Wartości niematerialne i prawne',
            'real_estates': 'Nieruchomości',
            'tools_machines': 'Maszyny i urządzenia',
            'transport': 'Środki transportu',
            'others': 'Inne aktywa rzeczowe trwałe',
            'materials_resources': 'Materiały i surowce',
            'products_halfproducts_in_progress': 'Produkty i półprodukty w toku',
            'ready_products': 'Produkty gotowe',
            'goods': 'Towary',
            'other_supplies': 'Pozostałe zapasy',
            'delivery_debts': 'Należności z tytułu dostaw i usług',
            'owner_debts': 'Należności od właściciela',
            'money': 'Środki pieniężne w kasie i w banku',
            'other_current_assets': 'Inne aktywa trwałe'
        }


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
        labels = {
            'own_capitals': 'Kapitały własne',
            'stopped_profit_of_own_capitals': 'Zysk zatrzymany kapitałów własnych',
            'long_term_liabilities': 'Zobowiązania długoterminowe',
            'long_term_borrowings': 'Pożyczki wchodzące w skład zobowiązań długoterminowych',
            'short_term_borrowings': 'Pożyczki i kredyty krótkoterminowe',
            'towards_suppliers': 'Zobowiązania krótkoterminowe wobec dostawców',
            'outdated_towards_suppliers': 'Przeterminowane zobowiązania wobec dostawców',
            'towards_budget': 'Zobowiązania wobec budżetu',
            'towards_zus': 'Zobowiązania wobec ZUS',
            'other_short_term_liabilities': 'Pozostałe zobowiązania',
            'other_liabilities': 'Inne pasywa',
            'dotations': 'Dotacje'
        }


class AddNewProfitsLosesForm(ModelForm):
    def save(self, commit=True):
        if commit:
            user = self.cleaned_data.get('user')
            time = self.cleaned_data.get('time_period')
            self.instance.save(user=user, time_period=time)
            return self.instance

    class Meta:
        model = models.ProfitsLoses
        exclude = ['created_by', 'time_period', 'identifier', 'netto_income_sum', 'supply_change_sum',
                   'income_costs', 'gross_income', 'netto_income', 'stopped_costs', 'operating_expenses_sum']
        labels = {
            'operation_br_income': 'Przychody z działalności B+R',
            'products_netto_income': 'Przychody netto z produktów',
            'goods_materials_netto_income': 'Przychody netto z produktów i materiałów',
            'other_netto_income': 'Pozostałe przychody netto',
            'dotations': 'Dotacje',
            'depreciation': 'Amortyzacja',
            'materials_energy_use': 'Zużycie materiałów i energii',
            'foreign_services': 'Usługi obce',
            'taxes': 'Podatki i opłaty',
            'salaries': 'Wynagrodzenia z narzutami',
            'interesr_comissions': 'Koszty operacji finansowych',
            'interests': 'Odsetki z operacji finansowych',
            'sold_goods_values': 'Wartość sprzedanych towarów i materiałów',
            'other_expenses': 'Pozostałe wyydatki',
            'supply_beg_state': 'Zapas początkowy',
            'supply_end_state': 'Zapas końcowy',
            'income_tax': 'Podatek dochodowy',
            'owner_maintnance_costs': 'Koszty utrzymania właściciela',
            'redemption_of_fixed_assets': 'Umorzenie środków trwałych'
        }


class AddBusinessCharacteristicForm(ModelForm):

    def save(self, commit=True):
        user = self.cleaned_data.get('user')
        self.instance.save(user=user)
        return self.instance

    class Meta:
        model = models.BusinessCharacteristicModel
        exclude = ['created_by', 'identifier']
        labels = {
            'business_start_date': 'Data rozpoczęcia działalności',
            'story_subject_business': 'Historia i przedmiot działalności'
        }
        widgets = {
            'business_start_date': DateInput()
        }


class AddTypeOfEconomicActivityForm(ModelForm):

    def clean(self):
        cleaned_data = super(AddTypeOfEconomicActivityForm, self).clean()
        cell1_sum = sum([cleaned_data.get('main_operation1_cell1'), cleaned_data.get('main_operation2_cell1'),
                         cleaned_data.get('main_operation2_cell1'), cleaned_data.get('main_operation4_cell1')])
        cell2_sum = sum([cleaned_data.get('main_operation1_cell2'), cleaned_data.get('main_operation2_cell2'),
                         cleaned_data.get('main_operation3_cell2'), cleaned_data.get('main_operation4_cell2')])
        if cell1_sum != 100:
            raise ValidationError('Suma udziału procentowego ogólnej wartości przychodów ze sprzedaży musi'
                                  'sumować się do 100%')
        elif cell2_sum != 100:
            raise ValidationError('Suma udziału pracujących w ogólnej liczbie pracujących')
        else:
            return super(AddTypeOfEconomicActivityForm, self).clean()

    def save(self, commit=True):
        user = self.cleaned_data.get('user')
        self.instance.save(user=user)
        return self.instance

    class Meta:
        model = models.TypeOfEconomicActivityModel
        exclude = ['created_by', 'identifier']



class AddNewApplicantOfferOperationIncomeForm(ModelForm):

    def save(self, commit=True):
        user = self.cleaned_data.get('user')
        self.instance.save(user=user)
        return self.instance

    class Meta:
        model = models.ApplicantOfferOperationIncomeModel
        exclude = ['created_by', 'identifier']


class AddNewCurrentPlaceOnMarketForm(ModelForm):

    def clean(self):
        cleaned_data = super(AddNewCurrentPlaceOnMarketForm, self).clean()
        a4_sum = sum([cleaned_data.get('receiver1_share'), cleaned_data.get("receiver2_share"),
                      cleaned_data.get('receiver3_share'), cleaned_data.get('receiver4_share')])
        if int(a4_sum) != 100:
            print('będzie error ', a4_sum)
            raise ValidationError("Udział w przychodach ze sprzedaży musi sumować się do 100%")
        return super(AddNewCurrentPlaceOnMarketForm, self).clean()

    def save(self, commit=True):
        user = self.cleaned_data.get('user')
        self.instance.save(user=user)
        return self.instance

    class Meta:
        model = models.CurrentPlaceOnTheMarketModel
        exclude = ['created_by', 'identifier']


class AddNewThirdModuleTableForm(ModelForm):

    def save(self, commit=True):
        component = models.ThirdModuleMainComponentModel.objects.get(pk=int(self.cleaned_data.get('component_id')))
        self.instance.save(component=component)
        return self.instance

    class Meta:
        model = models.ThirdModuleTableComponentModel
        exclude = ['main_component']
