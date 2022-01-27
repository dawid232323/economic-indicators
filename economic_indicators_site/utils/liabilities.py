class Equity:

    def __init__(self, own_capitals, st_profit):
        self.own_capitals = own_capitals
        self.stopped_profit = st_profit


class LiabilitiesAndProvisions:

    def __init__(self, long_term_lia, loans, short_term_borr, tow_suppliers, outdated_tow_sup,
                 tow_budget, tow_ZUS, others):
        self.long_term_liabilities = long_term_lia
        self.loans_borrowings = loans
        self.short_term_borrowings = short_term_borr
        self.towards_suppliers = tow_suppliers
        self.outdeted_towards_suppliers = outdated_tow_sup
        self.towards_budget = tow_budget
        self.towards_zus = tow_ZUS
        self.others = others
        self.short_term_liabilities = 0

    def sum_short_term_liabilities(self):
        self.short_term_liabilities = sum([self.short_term_borrowings, self.towards_suppliers,
                                           self.towards_budget, self.towards_zus, self.others])
        return self.short_term_liabilities


class OtherLiabilities:

    def __init__(self, other_liabilities, dotations):
        self.other_liabilities = other_liabilities
        self.dotations = dotations
