class FixedAssets:

    def __init__(self, intangible_assets, estates, tools, transport, others):
        self.intangible_assets = intangible_assets
        self.tangible_fixed_assets = 0
        self.real_estates = estates
        self.tools_machines = tools
        self.transport = transport
        self.others = others
        self.conclusion = 0

    def sum_tangible_assets(self):
        self.tangible_fixed_assets = sum([self.real_estates, self.tools_machines, self.transport, self.others])

    def get_all_fixed_assets(self):
        if self.tangible_fixed_assets == 0:
            self.sum_tangible_assets()
        self.conclusion = self.tangible_fixed_assets + self.intangible_assets
        return self.conclusion


class CurrentAssets:

    def __init__(self, materials, progress_products, ready_products, goods, other_supplies,
                 del_debts, own_debts, money, other_assets):
        self.materials_resources = materials
        self.products_halfproducts_in_progress = progress_products
        self.ready_products = ready_products
        self.goods = goods
        self.other_supplies = other_supplies
        self.delivery_debts = del_debts
        self.owner_debts = own_debts
        self.money = money
        self.other_assets = other_assets
        self.supplies = 0
        self.debts = 0
        self.current_assets = 0

    def sum_supplies(self):
        self.supplies = sum([self.materials_resources, self.products_halfproducts_in_progress, self.ready_products,
                                 self.goods, self.other_supplies])
        return self.supplies

    def sum_debts(self):
        self.debts = sum([self.owner_debts, self.delivery_debts])
        return self.debts

    def sum_current_assets(self):
        if self.supplies == 0:
            self.sum_supplies()
        if self.debts == 0:
            self.sum_debts()
        self.current_assets = sum([self.supplies, self.debts, self.money, self.other_assets])
        return self.current_assets
