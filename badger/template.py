"""
Minimal abstraction around jinja2.
We need this abastraction to allow projects
to specify their own templates in the future.
"""
#from jinja2 import Environment, PackageLoader
from jinja2 import Template
import os

class TemplateEngine:
    """
    Tiny wrapper around jinja2 to avoid having to specify environment settings
    everywhere.
    """
    def __init__(self, template_paths):
        """
        @template_paths list of paths to look for templates in
        """
        self.engine_name = "template"
        self.template_paths = template_paths
        #self.env = Environment(loader=PackageLoader('badger', 'templates'))

    def get(self, template):
        """
        Returns a jinja2 Template object on success, else None
        """
        for path in self.template_paths:
            filename = os.path.join(path, template)
            if os.path.isfile(filename):
                # read file, call continue on failure
                try:
                    fp = open(filename, "r")
                    template_data = fp.read()

                    return Template(template_data)

                except IOError, why:
                    continue
        return None
