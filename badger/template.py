"""
Minimal abstraction around jinja2.
We need this abastraction to allow projects
to specify their own templates in the future.
"""
from jinja2 import Environment, PackageLoader
from jinja2 import Template

class TemplateEngine:
    """
    Tiny wrapper around jinja2 to avoid having to specify environment settings
    everywhere.
    """
    def __init__():
        self.env = Environment(loader=PackageLoader('badger', 'templates'))

    def get_template(template):
        return env.get_template(template)
