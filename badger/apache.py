class ApacheEngine:
    def __init__(self, server, binary="/usr/sbin/apache2ctl"):
        self.engine_name = "apache"
        self.binary = binary

    def restart(self):
        run("sudo {0} restart",format(binary))

    def verify_site(site):

    def generate_site_vhost(site):


    def generate_platform_vhost(platform):

    def remove_site(site):
        run("rm config/apache/sites/{0}.conf", site.name)

    def remove_platform(platform):
        run("rm config/apache/platforms/{0}.conf", platform.name)
