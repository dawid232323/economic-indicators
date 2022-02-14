import assets
import liabilities
import profits_loses


class RaportGenerator:

    def __init__(self, fixed_ssets: assets.FixedAssets, current_assets: assets.CurrentAssets,
                 equity: liabilities.Equity, liabilities_provisions: liabilities.LiabilitiesAndProvisions,
                 other_liabilities: liabilities.OtherLiabilities, profit_loses_calc: profits_loses.Calculator,
                 netto_income: profits_loses.NettoIncome, operating_expenses: profits_loses.OperatingExpenses,
                 supply_change: profits_loses.SupplyChange):
        self.debt_ratio = 0 # wskaznik zadluzenia
        self.profitability_of_revenue_ratio = 0 # wskaznik rentownosci obrotu
        self.return_on_assets_ratio = 0 # wskaznik rentownosci majatku
        self.liquidity_ratio = 0 # wskaznik plynnosci
        self.fixed_assets = fixed_ssets
        self.current_assets = current_assets
        self.equity = equity
        self.liabilities_provisions = liabilities_provisions
        self.other_liabilities = other_liabilities
        self.profit_loses_calc = profit_loses_calc
        self.netto_income = netto_income
        self.operating_expenses = operating_expenses
        self.supply_change = supply_change
        self.money_surplus = 0 # relacja nadwyzek pienieznych
        self.bilans_sh_lil_ratio = 0 # stosunek sumy bilansowej
        self.financial_prop_score = 0 # relacja wyniku finansowegodo do majatku
        self.financial_sc_sales_rel = 0 # relacja wyniku finansowego
        self.supp_rev_relation = 0 # relacja zapasow
        self.assets_rotation = 0 # relacja sprzedazy do aktywow
        self.company_assessment = 0 # ocena przedsiebiorstwa

    def calculate_money_surplus(self):
        parameter = self.liabilities_provisions.sum_short_term_liabilities()\
                    + self.liabilities_provisions.long_term_liabilities
        if parameter == 0:
            return 0
        else:
            self.money_surplus = \
                (self.operating_expenses.depreciation + self.profit_loses_calc.sum_gross_income()) / parameter
            return self.money_surplus

    def calculate_bilans_short_liabelities_ratio(self):
        parameter = self.liabilities_provisions.sum_short_term_liabilities()\
                    + self.liabilities_provisions.long_term_liabilities
        if parameter == 0:
            return 0
        else:
            assets_sum = self.fixed_assets.get_all_fixed_assets() + self.current_assets.sum_current_assets()
            self.bilans_sh_lil_ratio = assets_sum / parameter
            return self.bilans_sh_lil_ratio

    def calculate_financial_property_score(self):
        parameter = self.fixed_assets.get_all_fixed_assets() + self.current_assets.sum_current_assets()
        if parameter == 0:
            return 0
        else:
            self.financial_prop_score = self.profit_loses_calc.sum_gross_income() / parameter
            return self.financial_prop_score

    def calculate_financial_score_sales_relation(self):
        parameter = self.netto_income.sum_netto_sales_income()
        if parameter == 0:
            return 0
        else:
            self.financial_sc_sales_rel = self.profit_loses_calc.sum_gross_income() / parameter
            return self.financial_sc_sales_rel

    def calculate_supplies_revenue_relation(self):
        parameter = self.netto_income.sum_netto_sales_income()
        if parameter == 0:
            return 0
        else:
            self.supp_rev_relation = self.current_assets.sum_supplies() / parameter
            return self.supp_rev_relation

    def calculate_assets_rotation(self):
        assets_sum = self.fixed_assets.get_all_fixed_assets() + self.current_assets.sum_current_assets()
        if assets_sum == 0:
            return 0
        else:
            self.assets_rotation = self.netto_income.sum_netto_sales_income() / assets_sum
            return self.assets_rotation

    def calculate_company_assesment(self):
        self.company_assessment = sum([1.5 * self.money_surplus, 0.08 * self.bilans_sh_lil_ratio,
                                       10 * self.financial_prop_score, 5 * self.financial_sc_sales_rel,
                                       0.3 * self.supp_rev_relation, 0.1 * self.assets_rotation])
        return self.company_assessment

    def get_company_prediction(self):
        if self.company_assessment < 0:
            return 'zagrożone upadłością'
        elif self.company_assessment == 0:
            return 'bardzo słaba'
        elif self.company_assessment in range(0, 1):
            return 'słaba'
        elif self.company_assessment in range(1, 2):
            return 'dobra'
        else:
            return 'bardzo dobra'

    def calculate_liquidity_ratio(self):
        parameter = self.liabilities_provisions.sum_short_term_liabilities()
        if parameter == 0:
            return 0
        else:
            self.liquidity_ratio = self.current_assets.sum_current_assets() / parameter
            return self.liquidity_ratio

    def calculate_return_on_assets_ratio(self):
        parameter = self.fixed_assets.get_all_fixed_assets() + self.current_assets.sum_current_assets()
        if parameter == 0:
            return 0
        else:
            print('in else')
            self.return_on_assets_ratio: float = self.profit_loses_calc.sum_netto_income() / parameter
            return self.return_on_assets_ratio

    def calculate_profitability_of_revenue_ratio(self):
        parameter = self.netto_income.sum_netto_sales_income()
        if parameter == 0:
            return 0
        else:
            self.profitability_of_revenue_ratio = self.profit_loses_calc.sum_netto_income() / parameter
            return self.profitability_of_revenue_ratio

    def calculate_debt_ratio(self):
        parameter = self.fixed_assets.get_all_fixed_assets() + self.current_assets.sum_current_assets()
        if parameter == 0:
            return 0
        else:
            self.debt_ratio = (self.liabilities_provisions.sum_short_term_liabilities()
                               + self.liabilities_provisions.long_term_liabilities) / parameter
            return self.debt_ratio
