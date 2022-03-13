from django.views.generic.base import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.models import User
from django.views.generic import View

from . import forms
from . import models
from .utils.raport_components import profits_loses, assets, liabilities, functions
from .utils.generators.to_pdf_model_generator import ReportPDFGenerator

import mimetypes

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
    template_name = 'economic_indicators_site/addCompSysUser.html'
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
        form.cleaned_data['user'] = self.request.GET.get('username')
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

    def __prepare_staff_context(self, context: dict):
        financial_analysis = []
        market_analysis = []
        internal_analysis = []
        for company in models.Company.objects.all():
            company_raports = models.FinalRaport.objects.filter(created_by__company=company)
            company_market_analysis = models.FullMarketAnalysisModel.objects.filter(created_by__company=company)
            company_internal_processes = models.ThirdModuleRaport.objects.filter(created_by__company=company)
            financial_analysis.append({'company': company.company_name, 'raports': company_raports})
            market_analysis.append({'company': company.company_name, 'raports': company_market_analysis})
            internal_analysis.append({'company': company.company_name, 'raports': company_internal_processes})
        context['financial'] = financial_analysis
        context['market'] = market_analysis
        context['internal'] = internal_analysis


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_system_user = models.CompanySystemUser.objects.get(user__username=self.request.user.username)
        if self.request.user.is_staff:
            context['is_admin'] = True
            self.__prepare_staff_context(context)
        else:
            context['is_admin'] = False
            raports = models.FullRaportBlock.objects.filter(created_by=current_system_user)
            context['raports'] = models.FinalRaport.objects.filter(
                identifier__startswith=str(current_system_user.user.id))
            context['market_analysis'] = models.FullMarketAnalysisModel.objects.filter(
                identifier__startswith=str(current_system_user.user_id))
            context['internal_proceses'] = models.ThirdModuleRaport.objects.filter(
                identifier__startswith=str(current_system_user.user_id))
        context['username'] = self.request.user.username
        context['user_id'] = int(current_system_user.user.id)
        context['time_periods'] = TIME_PERIODS
        # context['raports'] = models.FullRaport.objects.filter(company_id=current_system_user.company.id)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            self.template_name = 'economic_indicators_site/adminHomePage.html'
        return super().get(request)


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
                                calculator, for_year):
        new_raport_block = models.FullRaportBlock()
        username = self.request.user
        identifier = self.proper_identifier + "." + str(time_period)
        new_raport_block.save(user=username, time_period=time_period, identifier=identifier, fixed_assets=fixed_assets,
                              current_assets=current_assets, equity=equity, liabilities_provisions=liabilities_provisions,
                              other_liabilities=other_liabilities, profit_loses_calc=calculator, netto_income=netto_income,
                              operating_expenses=operating_expanses, supply_change=supply_change, for_year=for_year)
        return new_raport_block.id

    def __generate_block_raport(self, assets, liabilities, profits_loses, num):
        assets_instances = self.__assets_instances_generator(assets)
        liabilities_instances = self.__liabilities_instances_generator(liabilities)
        profits_loses_instances = self.__profits_loses_instances_generator(profits_loses)
        return self.__save_block_raport( num + 1, assets_instances[0], assets_instances[1], liabilities_instances[0],
                                  liabilities_instances[1], liabilities_instances[2], profits_loses_instances[0],
                                  profits_loses_instances[1], profits_loses_instances[2], profits_loses_instances[3], assets.created_at)

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
    template_name = 'economic_indicators_site/raports/fullRaportTemplate.html'

    def get_context_data(self, **kwargs):
        context = super(FullRaportView, self).get_context_data(**kwargs)
        identifier = self.request.GET.get('identifier')
        context['raport_blocks'] = models.FullRaportBlock.objects.filter(identifier__contains=identifier).all()
        context['id'] = identifier
        return context

class GenerateRaportFileView(LoginRequiredMixin, View):
    url = '/home'
    login_url = '/login'

    def __check_file_existance(self, id):
        file = None
        try:
            file = models.RaportFileModel.objects.get(identifier=id)
            return file
        except:
            query = models.FullRaportBlock.objects.filter(identifier__contains=self.request.GET.get('identifier'))
            file_name = ReportPDFGenerator(query, f'analiza_finansowa_{id}', self.request.user).generate()
            new_file_model = models.RaportFileModel(identifier=id, file_path=file_name)
            new_file_model.save()
            return new_file_model

    def get(self, request, *args, **kwargs):
        file_name = self.__check_file_existance(request.GET.get('identifier'))
        response = FileResponse(open(file_name.file_path, 'rb'))
        return response


class AddNewSecondModuleRaportBlockView(LoginRequiredMixin, FormView):
    template_name = 'economic_indicators_site/forms/basicForm.html'
    login_url = '/login'
    success_url = ''
    title = ''

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        form.save()
        return super(AddNewSecondModuleRaportBlockView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddNewSecondModuleRaportBlockView, self).get_context_data()
        context['subject'] = self.title
        return context

class BusinessCharacteristicView(AddNewSecondModuleRaportBlockView):
    form_class = forms.AddBusinessCharacteristicForm
    title = 'Uzupełnij Charakterystykę Przedsiębiorstwa'
    success_url = '/add_type_economic_activity'


class TypeOfEconomicActivityView(AddNewSecondModuleRaportBlockView):
    form_class = forms.AddTypeOfEconomicActivityForm
    template_name = 'economic_indicators_site/forms/tableForm.html'
    title = 'Uzupełnij Rodzaj Działalności Gospodarczej Przedsiębiorstwa'
    success_url = '/add_applicant_op_income'


class ApplicantOfferOpeartionIncomeView(AddNewSecondModuleRaportBlockView):
    form_class = forms.AddNewApplicantOfferOperationIncomeForm
    title = 'Uzupełnij Ofertę Wnioskodawcy i przychody z działalności'
    success_url = '/add_curent_place_on_market'


class CurrentPlaceOnTheMarketView(AddNewSecondModuleRaportBlockView):
    form_class = forms.AddNewCurrentPlaceOnMarketForm
    title = 'Uzupełnij Obecne Miejsce Na Rynku'
    success_url = '/generate_market_analisis_raport'


class GenerateMarketAnalysisRaport(LoginRequiredMixin, RedirectView):
    login_url = '/login'
    url = '/home'

    def get(self, request, *args, **kwargs):
        current_user = models.CompanySystemUser.objects.get(user__username=request.user)
        temp_identifier = functions.identify(current_user.user_id, current_user.second_module_raports, 0)
        functions.clearify(models.FullMarketAnalysisModel, temp_identifier)
        print(temp_identifier)
        new_instance = models.FullMarketAnalysisModel()
        new_instance.save(user=request.user)
        return super(GenerateMarketAnalysisRaport, self).get(request)


class MarketAnalysisView(LoginRequiredMixin, TemplateView):
    template_name = 'economic_indicators_site/raports/MarketAnalysisRaport.html'
    login_url = '/login'
    analysis_model: models.FullMarketAnalysisModel = None

    def get_context_data(self, **kwargs):
        context = super(MarketAnalysisView, self).get_context_data()
        if self.analysis_model is not None:
            context['id'] = self.analysis_model.id
            context['business_characteristics'] = self.analysis_model.characteristic_module
            context['economic_activity'] = self.analysis_model.operation_type_module
            context['applicant_offer'] = self.analysis_model.applicant_offer_module
            context['place_on_market'] = self.analysis_model.place_on_market_module
        else:
            print('none')
        return context

    def get(self, request, id=None, *args, **kwargs):
        self.analysis_model = models.FullMarketAnalysisModel.objects.get(pk=id)
        # print(self.analysis_model.get_serialised_data())
        return super(MarketAnalysisView, self).get(request, id)

class GenerateMarketAnalysisFileView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, id=None, *args, **kwargs):
        object = models.FullMarketAnalysisModel.objects.get(pk=id)
        if object.file_path is None:
            data = object.get_serialised_data()
            path = ReportPDFGenerator(None, f'analiza_rynkowa_{object.identifier}', request.user).generate_market_analysis(data)
            object.file_path = path
            object.save(update_fields=True, user=request.user)
        return FileResponse(open(object.file_path, 'rb'))


class ThirdModuleBaseView(LoginRequiredMixin, FormView):
    form_class = forms.AddNewThirdModuleTableForm
    template_name = 'economic_indicators_site/forms/ThirdModuleForm.html'
    login_url = '/login'
    base_url = ''
    component_name = ''
    next_url = ''
    type = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.component_name
        if 'rep' in self.request.GET:
            context['is_repetitive'] = True
        else:
            context['is_repetitive'] = True
        return context

    def form_valid(self, form):
        if 'comp_id' in self.request.GET:
            form.cleaned_data['component_id'] = self.request.GET.get('comp_id')
        else:
            new_instance = models.ThirdModuleMainComponentModel(name=self.component_name, type=self.type)
            new_instance.save(user=self.request.user)
            form.cleaned_data['component_id'] = new_instance.id
        if 'next' in self.request.POST:
            self.success_url = self.next_url
        else:
            self.success_url = f'{self.base_url}?comp_id={form.cleaned_data.get("component_id")}&rep=1'
        form.save()
        return super().form_valid(form)

class AddA1ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a1/'
    component_name = 'Czas wprowadzenia nowości na rynek'
    next_url = '/add_third_a2/'
    type = 1


class AddA2ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a2/'
    component_name = 'Czas składania zamówień'
    next_url = '/add_third_a3/'
    type = 2


class AddA3ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a3/'
    component_name = 'Czas zarządzania realizacją zamówień'
    next_url = '/add_third_a4/'
    type = 3


class AddA4ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a4/'
    component_name = 'Czas obsługi promocji i wyprzedaży'
    next_url = '/add_third_a5/'
    type = 4


class AddA5ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a5/'
    component_name = 'Czas zarządzania stanami magazynowymi, w tym wirtualnymi'
    next_url = '/add_third_a6/'
    type = 5


class AddA6ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a6/'
    component_name = 'Czas obsługi reklamacji'
    next_url = '/add_third_a7/'
    type = 6


class AddA7ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a7/'
    component_name = 'Czas udostępniania oferty handlowej potencjalnym kontrahentom'
    next_url = '/add_third_a8/'
    type = 7


class AddA8ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a8/'
    component_name = 'Czas realizacji dostaw, w tym śledzenia przesyłek i dostaw'
    next_url = '/add_third_a9/'
    type = 8


class AddA9ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a9/'
    component_name = 'Czas zarządzania oraz realizacji programu lojalnościowego'
    next_url = '/add_third_a10/'
    type = 9


class AddA10ThirdModuleView(ThirdModuleBaseView):
    base_url = '/add_third_a10/'
    component_name = 'Czas opisywania i aktualizacji bazy produktowej'
    next_url = '/generate_third_module_raport/'
    type = 10


class GenerateThirdModuleRaport(LoginRequiredMixin, RedirectView):
    login_url = '/login'
    url = '/home'
    template_name = 'economic_indicators_site/raports/ThirdModuleRaport.html'
    title = 'Analizy Procesów Wenętrznych'

    def get(self, request, *args, **kwargs):
        logged_user = models.CompanySystemUser.objects.get(user__username=self.request.user)
        temp_identifier = f'{logged_user.user.id}.{logged_user.third_module_raports}'
        print(temp_identifier)
        raport_blocks = models.ThirdModuleMainComponentModel.objects.filter(identifier__startswith=temp_identifier)
        print(raport_blocks)
        new_instance = models.ThirdModuleRaport(created_by=logged_user, identifier=temp_identifier,
                                                a1=raport_blocks[0], a2=raport_blocks[1], a3=raport_blocks[2],
                                                a4=raport_blocks[3], a5=raport_blocks[4], a6=raport_blocks[5],
                                                a7=raport_blocks[6], a8=raport_blocks[7], a9=raport_blocks[8],
                                                a10=raport_blocks[9])
        new_instance.save()
        logged_user.third_module_raports += 1
        logged_user.save(user=logged_user.user.username)
        return super(GenerateThirdModuleRaport, self).get(request, *args, **kwargs)



class ThirdModuleRaportView(LoginRequiredMixin, TemplateView):
    template_name = 'economic_indicators_site/raports/ThirdModuleRaport.html'
    login_url = '/login'
    raport_model: models.ThirdModuleRaport = None

    def get_context_data(self, **kwargs):
        context = super(ThirdModuleRaportView, self).get_context_data()
        if self.raport_model is not None:
            context['id'] = self.raport_model.id
            context['a1_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a1)
            context['a2_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a2)
            context['a3_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a3)
            context['a4_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a4)
            context['a5_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a5)
            context['a6_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a6)
            context['a7_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a7)
            context['a8_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a8)
            context['a9_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a9)
            context['a10_table'] = models.ThirdModuleTableComponentModel.objects.filter(main_component=self.raport_model.a10)
        return context

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            self.raport_model = models.ThirdModuleRaport.objects.get(id=int(id))
        return super().get(request, id=id, *args, **kwargs)

class GenerateThirdModuleFileView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, id=None, *args, **kwargs):
        object = models.ThirdModuleRaport.objects.get(id=id)
        logged_user = models.CompanySystemUser.objects.get(user__username=request.user)
        if object.file_path is None:
            new_path = ReportPDFGenerator(None, f'analiza_procesów_wewnętrznych_{object.identifier}', request.user).generate_third_module_file(object)
            object.file_path = new_path
            object.save()
        return FileResponse(open(object.file_path, 'rb'))


class AddCompanyView(LoginRequiredMixin, FormView):
    template_name = 'economic_indicators_site/forms/addCompanyForm.html'
    form_class = forms.AddCompanyForm
    login_url = '/login'
    success_url = '/home'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        print(user, ' user')
        self.success_url = f'/login/choose_company/?username={user.username}'
        return super(AddCompanyView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.success_url = f'/login/choose_company/?username={self.request.user}'
        context = super(AddCompanyView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.save()
        self.success_url = f'/login/choose_company/?username={self.request.user}'
        return super(AddCompanyView, self).form_valid(form)