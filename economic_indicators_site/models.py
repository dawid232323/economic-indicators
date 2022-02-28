from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

from economic_indicators_site.utils.raport_components import assets, liabilities
from economic_indicators_site.utils.raport_components.functions import identify, clearify
from economic_indicators_site.utils.raport_components.profits_loses import NettoIncome, OperatingExpenses, SupplyChange, Calculator
from economic_indicators_site.utils.raport_components.raport_generator import RaportGenerator
from economic_indicators_site.utils.year_validators import max_value_current_year

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


class Company(models.Model):
    company_name = models.CharField(max_length=150, blank=False)
    company_nip = models.CharField(max_length=10)
    company_regon = models.CharField(max_length=14, blank=False)

    def __str__(self):
        return self.company_name


class SystemUser(User):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class CompanySystemUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    num_of_reports = models.IntegerField(null=False, default=0)
    second_module_raports = models.IntegerField(default=0)
    third_module_raports = models.IntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        logged_user = User.objects.get(username=kwargs['user'])
        self.user = logged_user
        kwargs.__delitem__('user')
        return super(CompanySystemUser, self).save(**kwargs)

    def __str__(self):
        return self.user.username

#TODO
# Create authorization mechanism that checks if any of existing raport blocks' identifiers
# matches the new one. If so the old one shold be deleted


class Assets(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    created_at = models.IntegerField(default=2022, validators=[MinValueValidator(2010), max_value_current_year])
    time_period = models.IntegerField()
    identifier = models.CharField(max_length=20, db_index=True)
    intangible_fixed_assets = models.FloatField(default=0)
    tangible_fixed_assets = models.FloatField()
    real_estates = models.FloatField(default=0)
    tools_machines = models.FloatField(default=0)
    transport = models.FloatField(default=0)
    others = models.FloatField(default=0)
    all_fixed_assets = models.FloatField()
    materials_resources = models.FloatField(default=0)
    products_halfproducts_in_progress = models.FloatField(default=0)
    ready_products = models.FloatField(default=0)
    goods = models.FloatField(default=0)
    other_supplies = models.IntegerField(default=0)
    delivery_debts = models.FloatField(default=0)
    owner_debts = models.FloatField(default=0)
    money = models.FloatField(default=0)
    other_current_assets = models.FloatField(default=0)
    sum_of_supplies = models.FloatField()
    sum_of_debts = models.FloatField()
    sum_of_current_assets = models.FloatField()

    class Meta:
        ordering = ['time_period']

    def save(self, **kwargs):
        company_system_user_instance = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = company_system_user_instance
        kwargs.__delitem__('user')
        self.time_period = kwargs['time_period']
        kwargs.__delitem__('time_period')
        self.identifier = identify(self.created_by.user.id, self.created_by.num_of_reports,
                                   self.time_period)
        fx_assets = assets.FixedAssets(self.intangible_fixed_assets, self.real_estates,
                                       self.tools_machines, self.transport, self.others)
        tang_assets = fx_assets.sum_tangible_assets()
        sum_assets = fx_assets.get_all_fixed_assets()
        self.tangible_fixed_assets = tang_assets
        self.all_fixed_assets = sum_assets
        curr_assets = assets.CurrentAssets(self.materials_resources, self.products_halfproducts_in_progress,
                                           self.ready_products, self.goods, self.other_supplies,
                                           self.delivery_debts, self.owner_debts, self.money, self.other_current_assets)
        self.sum_of_supplies = curr_assets.sum_supplies()
        self.sum_of_debts = curr_assets.sum_debts()
        self.sum_of_current_assets = curr_assets.sum_current_assets()
        clearify(Assets, self.identifier)
        return super(Assets, self).save(**kwargs)

    def __str__(self):
        return f'Assets with identifier {self.identifier}'


class Liabilities(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    time_period = models.IntegerField()
    identifier = models.CharField(max_length=10, db_index=True)
    own_capitals = models.FloatField(default=0)
    stopped_profit_of_own_capitals = models.FloatField(default=0)
    long_term_liabilities = models.FloatField(default=0)
    long_term_loans_borrowings = models.FloatField(default=0)
    short_term_borrowings = models.FloatField(default=0)
    towards_suppliers = models.FloatField(default=0)
    outdated_towards_suppliers = models.FloatField(default=0)
    towards_budget = models.FloatField(default=0)
    towards_zus = models.FloatField(default=0)
    other_short_term_liabilities = models.FloatField(default=0)
    other_liabilities = models.FloatField(default=0)
    dotations = models.FloatField(default=0)
    short_term_liabilities = models.FloatField()
    sum_liabilities_and_provisions = models.FloatField()

    class Meta:
        ordering = ['time_period']

    def __check_existance(self):
        try:
            old_instance = Liabilities.objects.get(identifier=self.identifier)
            old_instance.delete()
        except Exception as e:
            print('Existing instance not found')

    def save(self, **kwargs):
        logged_comp_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_comp_user
        self.time_period = kwargs['time_period']
        self.identifier = identify(self.created_by.user.id, self.created_by.num_of_reports,
                                   self.time_period)
        liabiliies_provisions = liabilities.LiabilitiesAndProvisions(self.long_term_liabilities,
                                                                     self.long_term_loans_borrowings,
                                                                     self.short_term_borrowings,
                                                                     self.towards_suppliers,
                                                                     self.outdated_towards_suppliers,
                                                                     self.towards_budget, self.towards_zus,
                                                                     self.other_short_term_liabilities)
        self.short_term_liabilities = liabiliies_provisions.sum_short_term_liabilities()
        self.sum_liabilities_and_provisions = liabiliies_provisions.sum_liabilities_and_provisions()
        self.__check_existance()
        kwargs.__delitem__('user')
        kwargs.__delitem__('time_period')
        clearify(Liabilities, self.identifier)
        return super(Liabilities, self).save(**kwargs)

    def __str__(self):
        return f'Liabilities with identifier {self.identifier}'


class ProfitsLoses(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    time_period = models.IntegerField()
    identifier = models.CharField(max_length=10, db_index=True)
    netto_income_sum = models.FloatField()
    operation_br_income = models.FloatField(default=0)
    products_netto_income = models.FloatField(default=0)
    goods_materials_netto_income = models.FloatField(default=0)
    other_netto_income = models.FloatField(default=0)
    dotations = models.FloatField(default=0)
    operating_expenses_sum = models.FloatField()
    depreciation = models.FloatField(default=0)
    materials_energy_use = models.FloatField(default=0)
    foreign_services = models.FloatField(default=0)
    taxes = models.FloatField(default=0)
    salaries = models.FloatField(default=0)
    interesr_comissions = models.FloatField(default=0)
    interests = models.FloatField(default=0)
    sold_goods_values = models.FloatField(default=0)
    other_expenses = models.FloatField(default=0)
    supply_change_sum = models.FloatField()
    supply_beg_state = models.FloatField(default=0)
    supply_end_state = models.FloatField(default=0)
    income_costs = models.FloatField()
    gross_income = models.FloatField()
    income_tax = models.FloatField(default=0)
    netto_income = models.FloatField()
    owner_maintnance_costs = models.FloatField(default=0)
    stopped_costs = models.FloatField()
    redemption_of_fixed_assets = models.FloatField(default=0)

    class Meta:
        ordering = ['time_period']

    def save(self, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.time_period = kwargs['time_period']
        kwargs.__delitem__('time_period')
        kwargs.__delitem__('user')
        self.identifier = identify(self.created_by.user.id, self.created_by.num_of_reports,
                                   self.time_period)
        netto_income = NettoIncome(self.operation_br_income, self.products_netto_income,
                                   self.goods_materials_netto_income, self.other_netto_income, self.dotations)
        self.netto_income_sum = netto_income.sum_netto_sales_income()
        operating_expenses = OperatingExpenses(self.depreciation, self.materials_energy_use, self.foreign_services,
                                               self.taxes, self.salaries, self.interesr_comissions, self.interests,
                                               self.sold_goods_values, self.other_expenses)
        self.operating_expenses_sum = operating_expenses.sum_operating_expenses()
        supply_change = SupplyChange(self.supply_beg_state, self.supply_end_state)
        self.supply_change_sum = supply_change.calculate_change()
        calc = Calculator(netto_income, operating_expenses, supply_change, self.income_tax,
                          self.owner_maintnance_costs, self.redemption_of_fixed_assets)
        self.income_costs = calc.sum_income_costs()
        self.gross_income = calc.sum_gross_income()
        self.netto_income = calc.sum_netto_income()
        self.stopped_costs = calc.sum_stopped_income()
        clearify(ProfitsLoses, self.identifier)
        if int(self.time_period) == 8:
            logged_user.num_of_reports += 1
            logged_user.save(user=logged_user.user.username)
        return super(ProfitsLoses, self).save(**kwargs)

    def __str__(self):
        return f'Profits loses with identifier {self.identifier}'


class FullRaportBlock(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    created_at = models.IntegerField(default=2022)
    time_period = models.IntegerField()
    identifier = models.CharField(max_length=10, db_index=True, null=False)
    money_surplus = models.FloatField(default=0)
    bilans_sh_lil_ratio = models.FloatField(default=0)
    financial_prop_score = models.FloatField(default=0)
    financial_sc_sales_rel = models.FloatField(default=0)
    supp_rev_relaton = models.FloatField(default=0)
    assets_rotation = models.FloatField(default=0)
    company_assessment = models.FloatField(default=0)
    liquidity_ratio = models.FloatField(default=0)
    return_on_assets_ratio = models.FloatField(default=0)
    profitability_of_revenue_ratio = models.FloatField(default=0)
    debt_ratio = models.FloatField(default=0)
    company_prediction = models.CharField(max_length=30)

    class Meta:
        ordering = ['time_period']

    def get_serialised_data(self):
        return {
            'Okres obrachunkowy': self.created_at,
            'Relacja nadwyżek pieniężnych do zobowiązań krótko i długoterminowych': "{:.2f}".format(self.money_surplus),
            'Stosunek sumy bilansowej do zobowiązań krótko i długoterminowych': "{:.2f}".format(self.bilans_sh_lil_ratio),
            'Relacja wyniku finansowego brutto do majątku': "{:.2f}".format(self.financial_prop_score),
            'Relacja wyniku finansowego brutto do sprzedaży': "{:.2f}".format(self.financial_sc_sales_rel),
            'Relacja zapasów do obrotów': "{:.2f}".format(self.supp_rev_relaton),
            'Relacja sprzedaży do aktywów': "{:.2f}".format(self.assets_rotation),
            'Ocena przedsiębiorstwa': "{:.2f}".format(self.company_assessment),
            'Opis oceny przedsiębiorstwa': self.company_prediction,
            'Wskaźnik płynności': "{:.2f}".format(self.liquidity_ratio),
            'Wskaźnik rentowności majątku': "{:.2%}".format(self.return_on_assets_ratio),
            'Wskaźnik rentowności obrotu': "{:.2%}".format(self.profitability_of_revenue_ratio),
            'Wskaźnik zadłużenia': "{:.2f}".format(self.debt_ratio)
        }

    def save(self, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.time_period = kwargs['time_period']
        self.identifier = kwargs['identifier']
        self.created_at = kwargs['for_year']
        clearify(FullRaportBlock, self.identifier)
        raport_generator = RaportGenerator(kwargs['fixed_assets'], kwargs['current_assets'], kwargs['equity'],
                                           kwargs['liabilities_provisions'], kwargs['other_liabilities'],
                                           kwargs['profit_loses_calc'], kwargs['netto_income'], kwargs['operating_expenses'],
                                           kwargs['supply_change'])
        self.money_surplus = raport_generator.calculate_money_surplus()
        self.bilans_sh_lil_ratio = raport_generator.calculate_bilans_short_liabelities_ratio()
        self.financial_prop_score = raport_generator.calculate_financial_property_score()
        self.financial_sc_sales_rel = raport_generator.calculate_financial_score_sales_relation()
        self.supp_rev_relaton = raport_generator.calculate_supplies_revenue_relation()
        self.assets_rotation = raport_generator.calculate_assets_rotation()
        self.company_assessment = raport_generator.calculate_company_assesment()
        self.company_prediction = raport_generator.get_company_prediction()
        self.liquidity_ratio = raport_generator.calculate_liquidity_ratio()
        self.return_on_assets_ratio = raport_generator.calculate_return_on_assets_ratio()
        self.profitability_of_revenue_ratio = raport_generator.calculate_profitability_of_revenue_ratio()
        self.debt_ratio = raport_generator.calculate_debt_ratio()

        kwargs.__delitem__('user')
        kwargs.__delitem__('time_period')
        kwargs.__delitem__('identifier')
        kwargs.__delitem__('fixed_assets')
        kwargs.__delitem__('current_assets')
        kwargs.__delitem__('equity')
        kwargs.__delitem__('liabilities_provisions')
        kwargs.__delitem__('other_liabilities')
        kwargs.__delitem__('profit_loses_calc')
        kwargs.__delitem__('netto_income')
        kwargs.__delitem__('operating_expenses')
        kwargs.__delitem__('supply_change')
        kwargs.__delitem__('for_year')

        return super(FullRaportBlock, self).save(**kwargs)

    def __str__(self):
        return f'Raport block with identifier {self.identifier}'


#TODO
# Supplement FullRaport model. One model should correspond to one time period.
# View that will display full raport should check
# If raport with such identifier already exists.
# If not it should generate 8 raport models each corresponding to the certain time period.
# RaportView should display these 8 given reports as table like in the excel example


class FinalRaport(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    identifier = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Raport wygenerowany {self.created_at}'


class RaportFileModel(models.Model):
    identifier = models.CharField(max_length=10, unique=True)
    file_path = models.FilePathField()

    def __str__(self):
        return f'Raport {self.identifier}'


class BusinessCharacteristicModel(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, unique=True, db_index=True)
    business_start_date = models.DateField()
    story_subject_business = models.TextField(max_length=2000)

    def save(self, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.identifier = identify(logged_user.user.id, logged_user.second_module_raports, 0)
        kwargs.__delitem__('user')
        clearify(BusinessCharacteristicModel, self.identifier)
        return super(BusinessCharacteristicModel, self).save(**kwargs)


class TypeOfEconomicActivityModel(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10)
    main_operation1 = models.IntegerField(default=0)
    main_operation1_characteristics = models.TextField(max_length=500)
    main_operation1_cell1 = models.IntegerField()
    main_operation1_cell2 = models.IntegerField()
    main_operation2 = models.IntegerField(default=0)
    main_operation2_characteristics = models.TextField(max_length=500)
    main_operation2_cell1 = models.IntegerField()
    main_operation2_cell2 = models.IntegerField()
    main_operation3 = models.IntegerField(default=0)
    main_operation3_characteristics = models.TextField(max_length=500)
    main_operation3_cell1 = models.IntegerField()
    main_operation3_cell2 = models.IntegerField()
    main_operation4 = models.IntegerField(default=0)
    main_operation4_characteristics = models.TextField(max_length=500)
    main_operation4_cell1 = models.IntegerField()
    main_operation4_cell2 = models.IntegerField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.identifier = identify(logged_user.user.id, logged_user.second_module_raports, 0)
        kwargs.__delitem__('user')
        clearify(TypeOfEconomicActivityModel, self.identifier)
        return super(TypeOfEconomicActivityModel, self).save(**kwargs)


class ApplicantOfferOperationIncomeModel(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10, db_index=True)
    goods_offered_now1 = models.CharField(max_length=100)
    income_penultimate_year_now1 = models.FloatField(default=0)
    income_last_year_now1 = models.FloatField(default=0)
    income_current_year_now1 = models.FloatField(default=0)
    notes1 = models.CharField(max_length=150, default='', blank=True)
    goods_offered_now2 = models.CharField(max_length=100, default=None, null=True, blank=True)
    income_penultimate_year_now2 = models.FloatField(default=0)
    income_last_year_now2 = models.FloatField(default=0)
    income_current_year_now2 = models.FloatField(default=0)
    notes2 = models.CharField(max_length=150, default='', blank=True)
    goods_offered_now3 = models.CharField(max_length=100, default=None, null=True, blank=True)
    income_penultimate_year_now3 = models.FloatField(default=0)
    income_last_year_now3 = models.FloatField(default=0)
    income_current_year_now3 = models.FloatField(default=0)
    notes3 = models.CharField(max_length=150, default='', blank=True)
    goods_stopped1 = models.CharField(max_length=100, default=None, null=True, blank=True)
    income_penultimate_year_stopped1 = models.FloatField(default=0)
    income_last_year_stopped1 = models.FloatField(default=0)
    income_current_year_stopped1 = models.FloatField(default=0)
    stopped_notes1 = models.CharField(max_length=150, default='', blank=True)
    goods_stopped2 = models.CharField(max_length=100, default=None, null=True, blank=True)
    income_penultimate_year_stopped2 = models.FloatField(default=0)
    income_last_year_stopped2 = models.FloatField(default=0)
    income_current_year_stopped2 = models.FloatField(default=0)
    stopped_notes2 = models.CharField(max_length=150, default='', blank=True)
    goods_stopped3 = models.CharField(max_length=100, default=None, null=True, blank=True)
    income_penultimate_year_stopped3 = models.FloatField(default=0)
    income_last_year_stopped3 = models.FloatField(default=0)
    income_current_year_stopped3 = models.FloatField(default=0)
    stopped_notes3 = models.CharField(max_length=150, default='', blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.identifier = identify(logged_user.user_id, logged_user.second_module_raports, 0)
        kwargs.__delitem__('user')
        clearify(ApplicantOfferOperationIncomeModel, self.identifier)
        return super(ApplicantOfferOperationIncomeModel, self).save(**kwargs)


class CurrentPlaceOnTheMarketModel(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10)
    receiver1 = models.CharField(max_length=100)
    receiver1_share = models.FloatField(default=100)
    receiver2 = models.CharField(max_length=100, null=True, blank=True)
    receiver2_share = models.FloatField(default=0, null=True, blank=True)
    receiver3 = models.CharField(max_length=100, null=True, blank=True)
    receiver3_share = models.FloatField(default=0, null=True, blank=True)
    receiver4 = models.CharField(max_length=100, null=True, blank=True)
    receiver4_share = models.FloatField(default=0, null=True, blank=True)
    clients_needs_expectations = models.TextField(max_length=2000)
    company_growth_possibilities = models.TextField(max_length=2000)
    company_concurency = models.TextField(max_length=2000)
    company_competitive_advantages = models.TextField(max_length=2000)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        print(kwargs['user'])
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.identifier = identify(logged_user.user_id, logged_user.second_module_raports, 0)
        kwargs.__delitem__('user')
        clearify(CurrentPlaceOnTheMarketModel, self.identifier)
        return super(CurrentPlaceOnTheMarketModel, self).save(**kwargs)


class FullMarketAnalysisModel(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    identifier = models.CharField(max_length=10, db_index=True)
    characteristic_module = models.ForeignKey(BusinessCharacteristicModel, on_delete=models.CASCADE)
    operation_type_module = models.ForeignKey(TypeOfEconomicActivityModel, on_delete=models.CASCADE)
    applicant_offer_module = models.ForeignKey(ApplicantOfferOperationIncomeModel, on_delete=models.CASCADE)
    place_on_market_module = models.ForeignKey(CurrentPlaceOnTheMarketModel, on_delete=models.CASCADE)
    file_path = models.FilePathField(null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        kwargs.__delitem__('user')
        if not update_fields or update_fields is None:
            self.created_by = logged_user
            self.identifier = identify(logged_user.user_id, logged_user.second_module_raports, 0)
            self.characteristic_module = BusinessCharacteristicModel.objects.get(identifier=self.identifier)
            self.operation_type_module = TypeOfEconomicActivityModel.objects.get(identifier=self.identifier)
            self.applicant_offer_module = ApplicantOfferOperationIncomeModel.objects.get(identifier=self.identifier)
            self.place_on_market_module = CurrentPlaceOnTheMarketModel.objects.get(identifier=self.identifier)
            logged_user.second_module_raports += 1
            logged_user.save(user=logged_user.user.username)
        update_fields = False
        return super(FullMarketAnalysisModel, self).save(**kwargs)

    def get_serialised_data(self):
        return [
            [
                {
                    "Data Rozpoczęcia Działalności": self.characteristic_module.business_start_date.__str__(),
                    "Historia i przedmiot działalności": self.characteristic_module.story_subject_business
                }
            ],
            [
                {
                    "Działalność główna/ w ramach projektu/pozostała": self.operation_type_module.main_operation1,
                    "Charakterystyka": self.operation_type_module.main_operation1_characteristics,
                    "Udział % w ostatnim roku obrotowym ogólnej wartości przychodów ze sprzedaży":
                        self.operation_type_module.main_operation1_cell1,
                    "Udział % pracyjących w ogólnej liczbie praujących": self.operation_type_module.main_operation1_cell2
                },
                {
                    "Działalność główna/ w ramach projektu/pozostała": self.operation_type_module.main_operation2,
                    "Charakterystyka": self.operation_type_module.main_operation2_characteristics,
                    "Udział % w ostatnim roku obrotowym ogólnej wartości przychodów ze sprzedaży":
                        self.operation_type_module.main_operation2_cell1,
                    "Udział % pracyjących w ogólnej liczbie praujących": self.operation_type_module.main_operation2_cell2
                },
                {
                    "Działalność główna/ w ramach projektu/pozostała": self.operation_type_module.main_operation3,
                    "Charakterystyka": self.operation_type_module.main_operation3_characteristics,
                    "Udział % w ostatnim roku obrotowym ogólnej wartości przychodów ze sprzedaży":
                        self.operation_type_module.main_operation3_cell1,
                    "Udział % pracyjących w ogólnej liczbie praujących": self.operation_type_module.main_operation3_cell2
                },
                {
                    "Działalność główna/ w ramach projektu/pozostała": self.operation_type_module.main_operation4,
                    "Charakterystyka": self.operation_type_module.main_operation4_characteristics,
                    "Udział % w ostatnim roku obrotowym ogólnej wartości przychodów ze sprzedaży":
                        self.operation_type_module.main_operation4_cell1,
                    "Udział % pracyjących w ogólnej liczbie praujących": self.operation_type_module.main_operation4_cell2
                }
            ],
            [
                {
                    "Produkt/Towar/Usługa": self.applicant_offer_module.goods_offered_now1,
                    "Wartość przychodów za przedostatni rok obrotowy": self.applicant_offer_module.income_penultimate_year_now1,
                    "Wartość przychodów za ostatni zamknięty rok obrotowy": self.applicant_offer_module.income_last_year_now1,
                    "Wartość przychodów za okres bieżący": self.applicant_offer_module.income_current_year_now1,
                    "Uwagi": self.applicant_offer_module.notes1
                },
                {
                    "Produkt/Towar/Usługa": self.applicant_offer_module.goods_offered_now2,
                    "Wartość przychodów za przedostatni rok obrotowy": self.applicant_offer_module.income_penultimate_year_now2,
                    "Wartość przychodów za ostatni zamknięty rok obrotowy": self.applicant_offer_module.income_last_year_now2,
                    "Wartość przychodów za okres bieżący": self.applicant_offer_module.income_current_year_now2,
                    "Uwagi": self.applicant_offer_module.notes2
                },
                {
                    "Produkt/Towar/Usługa": self.applicant_offer_module.goods_offered_now3,
                    "Wartość przychodów za przedostatni rok obrotowy": self.applicant_offer_module.income_penultimate_year_now3,
                    "Wartość przychodów za ostatni zamknięty rok obrotowy": self.applicant_offer_module.income_last_year_now3,
                    "Wartość przychodów za okres bieżący": self.applicant_offer_module.income_current_year_now3,
                    "Uwagi": self.applicant_offer_module.notes3
                }
            ],
            [
                {
                    "Produkt/Towar/Usługa": self.applicant_offer_module.goods_stopped1,
                    "Wartość przychodów za przedostatni rok obrotowy": self.applicant_offer_module.income_penultimate_year_stopped1,
                    "Wartość przychodów za ostatni zamknięty rok obrotowy": self.applicant_offer_module.income_last_year_stopped1,
                    "Wartość przychodów za okres bieżący": self.applicant_offer_module.income_current_year_stopped1,
                    "Uwagi": self.applicant_offer_module.stopped_notes1
                },
                {
                    "Produkt/Towar/Usługa": self.applicant_offer_module.goods_stopped2,
                    "Wartość przychodów za przedostatni rok obrotowy": self.applicant_offer_module.income_penultimate_year_stopped2,
                    "Wartość przychodów za ostatni zamknięty rok obrotowy": self.applicant_offer_module.income_last_year_stopped2,
                    "Wartość przychodów za okres bieżący": self.applicant_offer_module.income_current_year_stopped2,
                    "Uwagi": self.applicant_offer_module.stopped_notes2
                },
                {
                    "Produkt/Towar/Usługa": self.applicant_offer_module.goods_stopped3,
                    "Wartość przychodów za przedostatni rok obrotowy": self.applicant_offer_module.income_penultimate_year_stopped3,
                    "Wartość przychodów za ostatni zamknięty rok obrotowy": self.applicant_offer_module.income_last_year_stopped3,
                    "Wartość przychodów za okres bieżący": self.applicant_offer_module.income_current_year_stopped3,
                    "Uwagi": self.applicant_offer_module.stopped_notes3
                },
            ],
            [
                {
                    "Odbiorca": self.place_on_market_module.receiver1,
                    "% udział w przychodach ze sprzedaży": self.place_on_market_module.receiver1_share
                },
                {
                    "Odbiorca": self.place_on_market_module.receiver2,
                    "% udział w przychodach ze sprzedaży": self.place_on_market_module.receiver2_share
                },
                {
                    "Odbiorca": self.place_on_market_module.receiver3,
                    "% udział w przychodach ze sprzedaży": self.place_on_market_module.receiver3_share
                },
                {
                    "Odbiorca": self.place_on_market_module.receiver4,
                    "% udział w przychodach ze sprzedaży": self.place_on_market_module.receiver4_share
                }
            ],
            [
                {
                    "Oczekiwania i potrzeby klientów": self.place_on_market_module.clients_needs_expectations
                }
            ],
            [
                {
                    "Możliwości rozwojowe przedsiębiorstwa": self.place_on_market_module.company_growth_possibilities
                }
            ],
            [
                {
                    "Konkurencja przedsiębiorstwa": self.place_on_market_module.company_concurency
                }
            ],
            [
                {
                    "Przewagi konkurencyjne przedsiębiorstwa": self.place_on_market_module.company_competitive_advantages
                }
            ]
        ]

    def __str__(self):
        return f'Analiza rynkowa wygenerowana {self.created_at}'

    class Meta:
        ordering = ['-created_at']


class ThirdModuleMainComponentModel(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    type = models.IntegerField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        logged_user = CompanySystemUser.objects.get(user__username=kwargs['user'])
        self.created_by = logged_user
        self.identifier = identify(logged_user.user_id, logged_user.third_module_raports, self.type)
        clearify(ThirdModuleMainComponentModel, self.identifier)
        kwargs.__delitem__('user')
        return super(ThirdModuleMainComponentModel, self).save(**kwargs)

    def __str__(self):
        return self.name

    def get_serialised_data(self):
        corresponding_tables = ThirdModuleTableComponentModel.objects.filter(main_component=self)
        result = []
        for table in corresponding_tables:
            temp = {
                "Czynność": table.activity,
                "Jednostka": table.unit,
                "Czas Trwania": table.duration
            }
            result.append(temp)
        return result

    class Meta:
        ordering = ['type']


class ThirdModuleTableComponentModel(models.Model):

    TIME_UNITS = [
        ('h', 'Godzina'),
        ('d', 'Dzień'),
        ('w', 'Tydzień'),
        ('m', 'Miesiąc')
    ]

    main_component = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200)
    unit = models.CharField(max_length=10, choices=TIME_UNITS)
    duration = models.IntegerField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        self.main_component = kwargs['component']
        kwargs.__delitem__('component')
        print('saving')
        return super(ThirdModuleTableComponentModel, self).save(**kwargs)

    def __str__(self): return self.activity


class ThirdModuleRaport(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    identifier = models.CharField(max_length=10)
    a1 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a1')
    a2 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a2')
    a3 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a3')
    a4 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a4')
    a5 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a5')
    a6 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a6')
    a7 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a7')
    a8 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a8')
    a9 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a9')
    a10 = models.ForeignKey(ThirdModuleMainComponentModel, on_delete=models.CASCADE, related_name='a10')
    file_path = models.FilePathField(null=True, db_index=True)

    def __str__(self): return f'Raport wygenerowany {self.created_at}'
