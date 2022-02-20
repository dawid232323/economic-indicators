import pandas as pd

from jinja2 import Environment, FileSystemLoader
from economic_indicators_site.models import FullRaportBlock
from weasyprint import HTML


class ReportPDFGenerator:
    def __init__(self, query, file_name, username):
        self.env = Environment(loader=FileSystemLoader('economic_indicators_site/utils/generators/'))
        self.template = self.env.get_template('raport_template.html')
        self.query = query
        self.template_vars = {}
        self.file_name = f'raport_{file_name}_{username}'

    def create_html_table_from_query(self, query_set):
        result_array = []
        for query in query_set:
            print('adding ', query)
            result_array.append(query.get_serialised_data())
        df = pd.DataFrame.from_dict(result_array)
        outer_table = pd.pivot_table(df, index=result_array[0].keys())
        return outer_table

    def generate(self):
        outer_table = self.create_html_table_from_query(self.query)
        self.template_vars['title'] = 'Raport Oceny Przedsiębiorstwa'
        self.template_vars['data'] = outer_table.to_html()
        html_out = self.template.render(self.template_vars)
        HTML(string=html_out).write_pdf(f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf',
                                        stylesheets=['economic_indicators_site/utils/generators/typography.css'])
        return f'economic_indicators_site/static/economic_indicators_site/generated/{self.file_name}.pdf'








