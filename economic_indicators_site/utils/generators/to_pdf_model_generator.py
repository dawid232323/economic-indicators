
import pandas as pd

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


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

    def generate_raport_analysis(self, serialised_data):
        pass

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








