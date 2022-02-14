import assets
import liabilities
import profits_loses
import raport_generator

fixed_assets = assets.FixedAssets(0, 0, 0, 20.38, 20.91)
current_assets = assets.CurrentAssets(0, 0, 0, 657.71, 0, 0, 0, 428.28, 0)
equity = liabilities.Equity(827.28, 136.56)
liabilities_provisions = liabilities.LiabilitiesAndProvisions(200, 200, 0, 100, 0, 0, 0, 0)
other_liabilities = liabilities.OtherLiabilities(0, 0)
netto_income = profits_loses.NettoIncome(0, 4622.97, 0, 3.80, 0)
operating_expenses = profits_loses.OperatingExpenses(92.36, 3128.12, 3.61, 0, 312.29, 0, 0, 779.26, 0)
supply_change = profits_loses.SupplyChange(0, 0)
calculator = profits_loses.Calculator(netto_income, operating_expenses,supply_change,
                                      54.57, 120, 0)
generator = raport_generator.RaportGenerator(fixed_assets, current_assets, equity, liabilities_provisions,
                                             other_liabilities, calculator, netto_income, operating_expenses,
                                             supply_change)
results = [
    generator.calculate_money_surplus(),
    generator.calculate_bilans_short_liabelities_ratio(),
    generator.calculate_financial_property_score(),
    generator.calculate_financial_score_sales_relation(),
    generator.calculate_supplies_revenue_relation(),
    generator.calculate_assets_rotation(),
    generator.calculate_company_assesment(),
    generator.get_company_prediction(),
    generator.calculate_liquidity_ratio(),
    generator.calculate_return_on_assets_ratio(),
    generator.calculate_profitability_of_revenue_ratio(),
    generator.calculate_debt_ratio(),

]

print(results, sep='\n')
