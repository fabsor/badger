import os
from hashlib import md5
from fabric.api import sudo, put
from fabric.contrib.files import exists

class ApacheEngine:
    def __init__(self, server, binary="/usr/sbin/apache2ctl",
                 vhost_path="/etc/apache2/sites-enabled",
                 vhost_template="apache_vhost.template",
                 vhost_data = {}):
        self.engine_name = "apache"
        self.binary = binary
        self.vhost_path = vhost_path
        self.vhost_template = vhost_template
        self.vhost_data = vhost_data

    def service_control(self, action):
        sudo("{0} restart", format(self.binary, action))

    def verify_site(self, site):
        if not hasattr(site, "database"):
            site.apache = {}

        if not "vhost" in site.apache:
            site.apache["vhost"] = os.path.join(self.vhost_path,
                                                site.name + ".vhost")

        if self.add_site_vhost(site):
            self.service_control("graceful") # feels safer then restart.

    def add_site_vhost(self, site):
        with site.platform.server:
            # generate vhost
            te = site.platform.server.get_engine("template")[0]
            # FIXME: We really need to pick up site specfic stuff here, and
            # inserts etc
            vhost = te.get(self.vhost_template)

            if not vhost:
                # FIXME: Raise error here
                pass

            vhost = vhost.render(
                {"port": 80,
                 "webmaster_email": "sample@mail.com",
                 "webroot": site.platform.source_path})

            if exists(site.apache["vhost"]):
                # See if it's the same or if we need to update it
                # check md5 sum
                #   - if missmatch overwrite with new.
                #   - else return False
                remote_md5 = sudo("md5sum {0} | cut -f 1 -d ' '".format(
                        site.apache["vhost"]))
                local_md5 = md5(vhost).hexdigest()

                if remote_md5 == local_md5:
                    return False

            # Upload new vhost
            open("/tmp/badger-mushroom.vhost", "w+").write(vhost)
            put("/tmp/badger-mushroom.vhost", site.apache["vhost"])
            os.unlink("/tmp/badger-mushroom.vhost")
            return True

    def remove_site_vhost(self, site):
        sudo("rm {0}", site.apache["vhost"])
