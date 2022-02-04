from django.db import models
from django.contrib.auth.models import User

from economic_indicators_site.utils import assets, liabilities, profits_loses
from economic_indicators_site.utils.functions import identify

# Create your models here.

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

    def __str__(self):
        return self.user.username

#TODO
# Create authorization mechanism that checks if any of existing raport blocks' identifiers
# matches the new one. If so the old one shold be deleted


class Assets(models.Model):
    created_by = models.ForeignKey(CompanySystemUser, on_delete=models.CASCADE)
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
        if self.time_period == 8:
            company_system_user_instance.num_of_reports += 1
        return super(Assets, self).save(**kwargs)


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
        return super(Liabilities, self).save(**kwargs)



#TODO
# Supplement FullRaport model


class FullRaport(models.Model):
    pass
