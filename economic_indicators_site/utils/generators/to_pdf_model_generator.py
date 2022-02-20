import pandas as pd

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


class RaportPDFGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template('raport_template.html')
        self.template_vars = {}

    def generate(self):
        data = {
            "Imię": 'Dawid',
            'Nazwisko': 'Pylak'
        }
        df = pd.DataFrame.from_dict(data)
        self.template_vars['title': 'title']
        self.template_vars['data': df.to_html()]
        html_out = self.template.render(self.template_vars)
        HTML(string=html_out).write_pdf('test.pdf')


RaportPDFGenerator().generate()






