import os
from fabric.api import sudo, put
from fabric.contrib.files import exists


class ApacheEngine:
    def __init__(self, server, binary="/usr/sbin/apache2ctl",
                 vhost_path="/etc/apache2/sites-enabled",
                 vhost_template="templates/apache_vhost.template"):
        self.engine_name = "apache"
        self.binary = binary
        self.vhost_path = vhost_path

    def service_control(self, action):
        sudo("{0} restart", format(self.binary, action))

    def verify_site(self, site):
        if not hasattr(site, "database"):
            site.apache = {}

        if not "vhost" in site.apache:
            site.apache["vhost"] = os.path.join(self.vhost_path, site.name +
                                                ".vhost")

        if self.add_site_vhost(site):
            self.services_control("graceful") # feels safer then restart.

    def add_site_vhost(self, site):
        with site.platform.server:
            if exists(site.apache["vhost"]):
                return False

            # Fake
            open("/tmp/fake.vhost", "w+").write("Mah vhost is amazing")
            put("/tmp/fake.vhost", site.apache["vhost"])
            return True

    def remove_site_vhost(self, site):
        sudo("rm {0}", site.apache["vhost"])
