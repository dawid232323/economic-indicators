import pandas as pd

from jinja2 import Environment, FileSystemLoader


class RaportPDFGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('.'))
        self.template = self.env.get_template('raport_template.html')
        self.template_vars = {}






