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

    def restart(self):
        run("sudo {0} restart", format(binary))

    def verify_site(self, site):
        if not hasattr(site, "database"):
            site.apache = {}

        if not "vhost" in site.apache:
            site.apache["vhost"] = os.path.join(self.vhost_path, site.name +
                                                ".vhost")

        self.generate_site_vhost(site)

    def generate_site_vhost(self, site):
        with site.platform.server:
            if exists(site.apache["vhost"]):
                return

            # Fake
            open("/tmp/fake.vhost", "w+").write("Mah vhost is amazing")
            put("/tmp/fake.vhost", site.apache["vhost"])

    def remove_site(self, site):
        run("rm config/apache/sites/{0}.conf", site.name)

    def remove_platform(self, platform):
        run("rm config/apache/platforms/{0}.conf", platform.name)
