import unittest
import os
from badger.template import TemplateEngine

class TemplateTest(unittest.TestCase):
    """
    Tests for the template engine.
    """
    def testTemplating(self):
        """
        Generate some output and compare.
        """
        te = TemplateEngine(["tests/templates"])
        template = te.get("test.str")
        expected = open("tests/templates/test.out", "r").read()
        output = template.render({"name": "Tester"})

        self.assertEqual(expected, output)

    def testNoneExisting(self):
        """
        Try to load a non-existing template.
        """
        te = TemplateEngine(["tests/templates"])
        template = te.get("not-existent")

        self.assertIsNone(template)

    def vhostExists(self, site):
        with site.platform.server:
            return exists(site.apache["vhost"])

    def apacheRunning(self, site):
        with site.platform.server:
            return run("pgrep '^apache2$'") != ""
