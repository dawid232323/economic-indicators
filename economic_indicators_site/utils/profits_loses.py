class NettoIncome:

    def __init__(self, operationBR, products_income, goods_materials_income, other_income, donations):
        self.operationBR_income = operationBR
        self.products_netto_income = products_income
        self.goods_materials_netto_income = goods_materials_income
        self.other_netto_income = other_income
        self.donations = donations
        self.sum = 0

    def sum_netto_sales_income(self):
        self.sum = sum([self.products_netto_income, self.goods_materials_netto_income, self.other_netto_income])
        return self.sum

class OperatingExpenses:

    def __init__(self, depreciation, materials_energy_usage, foreign_services, taxes, salaries, interest_commissions,
                 interest, sold_goods_value, other_expenses):
        self.depreciation = depreciation
        self.materials_energy_usage = materials_energy_usage
        self.foreign_services = foreign_services
        self.taxes = taxes
        self.salaries = salaries
        self.interest_commissions = interest_commissions
        self.interest = interest
        self.sold_goods_value = sold_goods_value
        self.other_expenses = other_expenses
        self.operating_expenses = 0

    def sum_operating_expenses(self):
        self.operating_expenses = sum([self.depreciation, self.materials_energy_usage,
                                       self.taxes, self.salaries, self.interest_commissions, self.sold_goods_value,
                                       self.other_expenses])
        return self.operating_expenses


class SupplyChange:

    def __init__(self, beg_state, end_state):
        self.beg_state = beg_state
        self.end_state = end_state
        self.change = 0

    def calculate_change(self):
        self.change = self.end_state - self.beg_state
        return self.change


class Calculator:

    def __init__(self, netto_income: NettoIncome, operating_expenses: OperatingExpenses, supply_change: SupplyChange,
                 in_tax, own_main_cost, red_fixed_assets):
        self.income_tax = in_tax
        self.owners_maintnance_cost = own_main_cost
        self.redemption_of_fixed_assets = red_fixed_assets
        self.income_costs = operating_expenses.sum_operating_expenses() - supply_change.calculate_change()
        self.gross_income = netto_income.sum_netto_sales_income() - self.income_costs
        self.netto_income = self.gross_income - self.income_tax
        self.stopped_income = self.netto_income - self.owners_maintnance_cost
