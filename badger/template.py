"""
Minimal abstraction around jinja2.
We need this abastraction to allow projects
to specify their own templates in the future.
"""
from jinja2 import Environment, PackageLoader
from jinja2 import Template


def get_engine("templates"):
    env = Environment(loader=PackageLoader('DrushEngine', 'templates'))
    return env
    
