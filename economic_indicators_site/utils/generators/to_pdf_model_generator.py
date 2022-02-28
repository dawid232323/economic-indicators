
import pandas as pd

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from economic_indicators_site.models import ThirdModuleRaport


class ReportPDFGenerator:
    def __init__(self, query, file_name, username):
        self.env = Environment(loader=FileSystemLoader('economic_indicators_site/utils/generators/'))
        self.template = self.env.get_template('raport_template.html')
        self.query = query
        self.template_vars = {}
        self.file_name = f'{file_name}_{username}'

    def create_html_table_from_query(self, query_set):
        result_array = []
        for query in query_set:
            print('adding ', query)
            result_array.append(query.get_serialised_data())
        df = pd.DataFrame.from_dict(result_array)
        outer_table = pd.pivot_table(df, index=result_array[0].keys())
        return outer_table

    def __create_pivot_table(self, data_frame, index):
        table = pd.pivot_table(data_frame, index=list(index))
        return table

    def create_market_analysis_tables(self, serialised_data):
        company_characteristic = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[0]), serialised_data[0][0].keys())
        a2_table = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[1]), serialised_data[1][0].keys())
        a3_now_table = self.__create_pivot_table(pd.DataFrame(serialised_data[2]), serialised_data[2][0].keys())
        a3_stopped_table = self.__create_pivot_table(pd.DataFrame(serialised_data[3]), serialised_data[3][0].keys())
        a4_receivers_table = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[4]), serialised_data[4][0].keys())
        a4_needs_table = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[5]), serialised_data[5][0].keys())
        a4_opportunities_table = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[6]), serialised_data[6][0].keys())
        a4_concurency_table = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[7]), serialised_data[7][0].keys())
        a4_advantages_table = self.__create_pivot_table(pd.DataFrame.from_dict(serialised_data[8]), serialised_data[8][0].keys())

        self.template_vars['company_characteristic'] = company_characteristic.to_html()
        self.template_vars['a2_table'] = a2_table.to_html()
        self.template_vars['a3_now_table'] = a3_now_table.to_html()
        self.template_vars['a3_stopped_table'] = a3_stopped_table.to_html()
        self.template_vars['a4_receivers_table'] = a4_receivers_table.to_html()
        self.template_vars['a4_needs_table'] = a4_needs_table.to_html()
        self.template_vars['a4_opportunities_table'] = a4_opportunities_table.to_html()
        self.template_vars['a4_concurency_table'] = a4_concurency_table.to_html()
        self.template_vars['a4_advantages_table'] = a4_advantages_table.to_html()

    def __create_third_module_tables(self, raport_model: ThirdModuleRaport):
        a1_serialised = raport_model.a1.get_serialised_data()
        a1_table = self.__create_pivot_table(pd.DataFrame.from_dict(a1_serialised), index=a1_serialised[0].keys())
        a2_serialised = raport_model.a2.get_serialised_data()
        a2_table = self.__create_pivot_table(pd.DataFrame.from_dict(a2_serialised), index=a2_serialised[0].keys())
        a3_serialised = raport_model.a3.get_serialised_data()
        a3_table = self.__create_pivot_table(pd.DataFrame.from_dict(a3_serialised), index=a3_serialised[0].keys())
        a4_serialised = raport_model.a4.get_serialised_data()
        a4_table = self.__create_pivot_table(pd.DataFrame.from_dict(a4_serialised), index=a4_serialised[0].keys())
        a5_serialised = raport_model.a5.get_serialised_data()
        a5_table = self.__create_pivot_table(pd.DataFrame.from_dict(a5_serialised), index=a5_serialised[0].keys())
        a6_serialised = raport_model.a6.get_serialised_data()
        a6_table = self.__create_pivot_table(pd.DataFrame.from_dict(a6_serialised), index=a6_serialised[0].keys())
        a7_serialised = raport_model.a7.get_serialised_data()
        a7_table = self.__create_pivot_table(pd.DataFrame.from_dict(a7_serialised), index=a7_serialised[0].keys())
        a8_serialised = raport_model.a8.get_serialised_data()
        a8_table = self.__create_pivot_table(pd.DataFrame.from_dict(a8_serialised), index=a8_serialised[0].keys())
        a9_serialised = raport_model.a9.get_serialised_data()
        a9_table = self.__create_pivot_table(pd.DataFrame.from_dict(a9_serialised), index=a9_serialised[0].keys())
        a10_serialised = raport_model.a10.get_serialised_data()
        a10_table = self.__create_pivot_table(pd.DataFrame.from_dict(a10_serialised), index=a10_serialised[0].keys())

        self.template_vars['tables'] = [a1_table.to_html(), a2_table.to_html(), a3_table.to_html(), a4_table.to_html(), a5_table.to_html(),
                                        a6_table.to_html(), a7_table.to_html(), a8_table.to_html(), a9_table.to_html(), a10_table.to_html()]

        self.template_vars['titles'] = ['Czas wprowadzenia nowości na rynek', 'Czas składania zamówień',
                                        'Czas zarządzania realizacją zamówień', 'Czas obsługi promocji i wyprzedaży', 'Czas zarządzania stanami magazynowymi, w tym wirtualnymi',
                                        'Czas obsługi reklamacji', 'Czas udostępniania oferty handlowej potencjalnym kontrahentom',
                                        'Czas realizacji dostaw, w tym śledzenia przesyłek i dostaw', 'Czas zarządzania oraz realizacji programu lojalnościowego',
                                        'Czas opisywania i aktualizacji bazy produktowej']

    def generate_third_module_file(self, raport_model: ThirdModuleRaport):
        self.__create_third_module_tables(raport_model)
        self.template = self.env.get_template('third_module.html')
        html_out = self.template.render(self.template_vars)
        HTML(string=html_out).write_pdf(f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf',
                                        stylesheets=['economic_indicators_site/utils/generators/typography.css'])
        return f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf'

    def generate_market_analysis(self, serialised_data):
        self.template = self.env.get_template('market_analysis.html')
        self.create_market_analysis_tables(serialised_data)
        html_out = self.template.render(self.template_vars)
        HTML(string=html_out).write_pdf(f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf',
                                        stylesheets=['economic_indicators_site/utils/generators/typography.css'])
        return f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf'

    def generate(self):
        outer_table = self.create_html_table_from_query(self.query)
        self.template_vars['title'] = 'Raport Oceny Przedsiębiorstwa'
        self.template_vars['data'] = outer_table.to_html()
        html_out = self.template.render(self.template_vars)
        HTML(string=html_out).write_pdf(f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf',
                                        stylesheets=['economic_indicators_site/utils/generators/typography.css'])
        return f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf'








