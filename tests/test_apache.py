import unittest
import os
from mocks import MockEngine
from badger.apache import ApacheEngine
from badger.types import Site, Server, Platform
from badger.template import TemplateEngine
from fabric.api import run
from fabric.contrib.files import exists

class ApacheEngineTest(unittest.TestCase):
    """
    Test Apache engine. This requires an apache server
    """
    def testVerifySite(self):
        """
        Create a sample vhost for a site.
        """
        server = Server("127.0.0.1", "deployer")
        server.add_engine(MockEngine())
        server.add_engine(ApacheEngine(server, vhost_template="apache.vhost"))
        server.add_engine(TemplateEngine(["./tests/templates"]))
        platform = Platform("./testplatform", server)
        site = Site("example.com", platform, server)
        site.verify()

        self.assertTrue(self.vhostExists(site))
        self.assertTrue(self.apacheRunning(site))
        self.assertTrue(self.vhostOK(site))

    def vhostExists(self, site):
        with site.platform.server:
            return exists(site.apache["vhost"])

    def vhostOK(self, site):
        with site.platform.server:
            expected = open("./tests/templates/test.out", "r").read()
            return exists(site.apache["vhost"])

    def apacheRunning(self, site):
        with site.platform.server:
            return run("pgrep '^apache2$'") != ""
