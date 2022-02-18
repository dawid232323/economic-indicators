from django.views.generic.base import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User

from . import forms
from . import models
from .utils import assets, liabilities, profits_loses

TIME_PERIODS = {
    1: "Poprzedni okres obrachunkowy (x-3)",
    2: "Poprzedni okres obrachunkowy (x-2)",
    3: "Ostatni okres obrachunkowy (x-1)",
    4: 'Okres bieżący (x)',
    5: 'Prognoza na koniec okresu (x)',
    6: 'Prognoza na koniec kolejnego roku (x+1)',
    7: 'Prognoza na koniec kolejnego roku (x+2)',
    8: 'Prognoza na koniec kolejnego roku (x+3)'
}


class RegisterView(FormView):
    form_class = forms.UserRegisterForm
    template_name = 'economic_indicators_site/authentication/register_page.html'
    success_url = '/login'

    def form_valid(self, form):
        new_form = form.save()
        return super().form_valid(form)


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'economic_indicators_site/authentication/login_page.html'
    next_page = '/home'

    def form_valid(self, form):
        print(form.cleaned_data.get('username'))
        try:
            username = str(form.cleaned_data.get('username'))
            logged_user = User.objects.get(username=username)
            if not models.CompanySystemUser.objects.filter(user_id=logged_user.id).exists():
                self.next_page = f'choose_company/?username={username}'
            else:
                self.next_page = f'/home'
        except Exception as ex:
            logged_user = None
        finally:
            return super().form_valid(form)


class AddCompanySystemUserView(LoginRequiredMixin, CreateView):
    form_class = forms.AddUserCompanyForm
    template_name = 'economic_indicators_site/authentication/register_page.html'
    success_url = '/home'
    login_url = '/login'
    redirect_field_name = ''

    def get(self, request, *args, **kwargs):
        if models.CompanySystemUser.objects.filter(user__username=request.user.username).exists():
            return HttpResponseRedirect('/home')
        return super(AddCompanySystemUserView, self).get(request, *args, **kwargs)

#TODO
# Add custom error page that will tell the user that he cannot choose anyone but himself
    def form_valid(self, form):
        username = str(self.request.GET.get('username'))
        current_user = User.objects.get(username=username).username.replace(' ', '')
        cleaned_username = str(form.cleaned_data['user']).replace(' ', '')
        if cleaned_username != current_user:
            raise Exception
        else:
            return super(AddCompanySystemUserView, self).form_valid(form)


class RegisterNewUserView(SuccessMessageMixin, CreateView):
    form_class = forms.TestRegisterForm
    template_name = 'economic_indicators_site/authentication/register_page.html'
    success_url = '/login'
    success_message = 'User Created successfully'


class LogOutUser(LogoutView):
    next_page = '/login'
    template_name = 'economic_indicators_site/authentication/login_page.html'


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'economic_indicators_site/homePage.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_system_user = models.CompanySystemUser.objects.get(user__username=self.request.user.username)
        raports = models.FullRaportBlock.objects.filter(created_by=current_system_user)
        context['username'] = self.request.user.username
        context['raports'] = models.FinalRaport.objects.filter(identifier__startswith=str(current_system_user.user.id))
        context['user_id'] = int(current_system_user.user.id)
        context['time_periods'] = TIME_PERIODS
        # context['raports'] = models.FullRaport.objects.filter(company_id=current_system_user.company.id)
        return context


class CreateNewRaportBlockView(FormView):
    template_name = 'economic_indicators_site/forms/basicForm.html'
    page_title = 'Uzupełnij'

    def form_valid(self, form): #Here developer needs to fill the success_url
        form.cleaned_data['user'] = self.request.user
        form.cleaned_data['time_period'] = int(self.request.GET.get('number'))
        form.save()
        return super(CreateNewRaportBlockView, self).form_valid(form)

    def get_context_data(self, **kwargs): # Here user has to fill the page_title
        context = super(CreateNewRaportBlockView, self).get_context_data(**kwargs)
        context['subject'] = self.page_title
        return context


class AddNewAssetsView(LoginRequiredMixin, CreateNewRaportBlockView):
    template_name = 'economic_indicators_site/forms/basicForm.html'
    form_class = forms.AddNewAssetsForm
    login_url = '/login'
    success_url = '/new_raport/add_liabilities/'

    def form_valid(self, form):
        time_number = int(self.request.GET.get('number'))
        self.success_url = f'/new_raport/add_liabilities/?number={time_number}'
        return super(AddNewAssetsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        period = TIME_PERIODS[int(self.request.GET.get('number'))]
        self.page_title = f'Uzupełnij Aktywa za {period}'
        return super(AddNewAssetsView, self).get_context_data(**kwargs)


class AdddNewLiabilitiesView(LoginRequiredMixin, CreateNewRaportBlockView):
    template_name = 'economic_indicators_site/forms/basicForm.html'
    form_class = forms.AddNewLiabilities
    login_url = '/login'
    success_url = '/new_raport/add_profits_loses/'

    def get_context_data(self, **kwargs):
        period = TIME_PERIODS[int(self.request.GET.get('number'))]
        self.page_title = f'Uzupełnij Pasywa za {period}'
        return super(AdddNewLiabilitiesView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        time_number = int(self.request.GET.get('number'))
        self.success_url = f'/new_raport/add_profits_loses/?number={time_number}'
        return super(AdddNewLiabilitiesView, self).form_valid(form)


class AddNewProfitsLosesView(LoginRequiredMixin, CreateNewRaportBlockView):
    form_class = forms.AddNewProfitsLosesForm
    login_url = '/login'
    success_url = '/new_raport/add_assets'

    def get_context_data(self, **kwargs):
        period = TIME_PERIODS[int(self.request.GET.get('number'))]
        self.page_title = f'Uzupełnij Rachunek Zysków i Strat za {period}'
        return super(AddNewProfitsLosesView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        time_number = self.request.GET.get('number')
        if int(time_number) == 8:
            current_user = models.CompanySystemUser.objects.get(user__username=self.request.user)
            identifier = f"{current_user.user.id}.{current_user.num_of_reports}"
            self.success_url = f'/generate_raport/?identifier={identifier}'
        else:
            self.success_url = f'/new_raport/add_assets/?number={int(time_number) + 1}'
        return super(AddNewProfitsLosesView, self).form_valid(form)

class GenerateRaportView(LoginRequiredMixin, RedirectView):
    url = ''
    existing_raport_id = -1
    proper_identifier = ''
    login_url = '/login'

    def __check_raport_existance(self):
        id = self.request.GET.get('identifier')
        try:
            raport_identifier = models.FullRaportBlock.objects.get(identifier__contains=id)
            self.existing_raport_id = raport_identifier.id
            return True
        except:
            return False

    def __get_wanted_queries(self):
        assets = models.Assets.objects.filter(identifier__contains=self.proper_identifier)
        liababilities = models.Liabilities.objects.filter(identifier__contains=self.proper_identifier)
        profits_loses = models.ProfitsLoses.objects.filter(identifier__contains=self.proper_identifier)
        return assets, liababilities, profits_loses

    def __assets_instances_generator(self, assets_model: models.Assets):
        fixed_assets = assets.FixedAssets(assets_model.intangible_fixed_assets,
                                          assets_model.real_estates, assets_model.tools_machines,
                                          assets_model.transport, assets_model.others)
        current_assets = assets.CurrentAssets(assets_model.materials_resources, assets_model.products_halfproducts_in_progress,
                                              assets_model.ready_products, assets_model.goods, assets_model.other_supplies,
                                              assets_model.delivery_debts, assets_model.owner_debts, assets_model.money,
                                              assets_model.other_current_assets)
        return fixed_assets, current_assets

    def __liabilities_instances_generator(self, liabilities_model: models.Liabilities):
        equity = liabilities.Equity(liabilities_model.own_capitals, liabilities_model.stopped_profit_of_own_capitals)
        liabilities_provisions = liabilities.LiabilitiesAndProvisions(liabilities_model.long_term_liabilities,
                                                                      liabilities_model.long_term_loans_borrowings,
                                                                      liabilities_model.short_term_borrowings, liabilities_model.towards_suppliers,
                                                                      liabilities_model.outdated_towards_suppliers, liabilities_model.towards_budget,
                                                                      liabilities_model.towards_zus, liabilities_model.other_short_term_liabilities)
        other_liabilities = liabilities.OtherLiabilities(liabilities_model.other_liabilities,
                                                         liabilities_model.dotations)
        return equity, liabilities_provisions, other_liabilities

    def __profits_loses_instances_generator(self, profits_model: models.ProfitsLoses):
        netto_income = profits_loses.NettoIncome(profits_model.operation_br_income, profits_model.products_netto_income,
                                                 profits_model.goods_materials_netto_income, profits_model.other_netto_income,
                                                 profits_model.dotations)
        operating_expenses = profits_loses.OperatingExpenses(profits_model.depreciation, profits_model.materials_energy_use,
                                                             profits_model.foreign_services, profits_model.taxes, profits_model.salaries,
                                                             profits_model.interesr_comissions, profits_model.interests, profits_model.sold_goods_values,
                                                             profits_model.other_expenses)
        supply_change = profits_loses.SupplyChange(profits_model.supply_beg_state, profits_model.supply_end_state)
        calculator = profits_loses.Calculator(netto_income, operating_expenses, supply_change,
                                              profits_model.income_tax, profits_model.owner_maintnance_costs,
                                              profits_model.redemption_of_fixed_assets)
        return netto_income, operating_expenses, supply_change, calculator

    def __save_block_raport(self, time_period, fixed_assets, current_assets, equity, liabilities_provisions,
                                other_liabilities, netto_income, operating_expanses, supply_change,
                                calculator):
        new_raport_block = models.FullRaportBlock()
        username = self.request.user
        identifier = self.proper_identifier + "." + str(time_period)
        new_raport_block.save(user=username, time_period=time_period, identifier=identifier, fixed_assets=fixed_assets,
                              current_assets=current_assets, equity=equity, liabilities_provisions=liabilities_provisions,
                              other_liabilities=other_liabilities, profit_loses_calc=calculator, netto_income=netto_income,
                              operating_expenses=operating_expanses, supply_change=supply_change)
        return new_raport_block.id

    def __generate_block_raport(self, assets, liabilities, profits_loses, num):
        assets_instances = self.__assets_instances_generator(assets)
        liabilities_instances = self.__liabilities_instances_generator(liabilities)
        profits_loses_instances = self.__profits_loses_instances_generator(profits_loses)
        return self.__save_block_raport( num + 1, assets_instances[0], assets_instances[1], liabilities_instances[0],
                                  liabilities_instances[1], liabilities_instances[2], profits_loses_instances[0],
                                  profits_loses_instances[1], profits_loses_instances[2], profits_loses_instances[3])

    def get(self, request, *args, **kwargs):
        if self.__check_raport_existance():
            self.url = f'/raport/{self.existing_raport_id}'
            return super(GenerateRaportView, self).get(request, *args, **kwargs)
        else:
            self.url = '/home'
            self.proper_identifier = self.request.GET.get('identifier')
            assets, liabilities, profits_loses = self.__get_wanted_queries()
            for i in range(0, 8):
                self.__generate_block_raport(assets[i], liabilities[i], profits_loses[i], i)
            new_full_raport = models.FinalRaport(created_by=models.CompanySystemUser.objects.get(user__username=request.user),
                                                     identifier=self.proper_identifier)
            new_full_raport.save()
            return super(GenerateRaportView, self).get(request, *args, **kwargs)

class FullRaportView(TemplateView):
    template_name = 'economic_indicators_site/fullRaportTemplate.html'

    def get_context_data(self, **kwargs):
        context = super(FullRaportView, self).get_context_data(**kwargs)
        identifier = self.request.GET.get('identifier')
        context['raport_blocks'] = models.FullRaportBlock.objects.filter(identifier__contains=identifier)
        return context


