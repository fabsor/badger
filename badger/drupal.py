"""
Drupal specific implementations for platforms
and sites.
"""
from badger import Site, Server
from fabric.api import local, settings, abort, run, cd, sudo, put, env, prompt, get

class DrupalEngine:
    """
    Drupal uses drush for most things. this is a just a thin
    abstraction layer around it.
    """

    def backup(self, site, path):
        local("drush @{0} archive-dump {0} --destination={1}".format(site.name, path))

    def clone(self, site, new_site):
        # Copy the existing site over.
        if site.platform.server == site.platform.server:
            run("cp -R {0} {1}".format(site.path, new_site.path))
        else:
            with site.platform.server:
                run("tar -zcf /tmp/{0}.tar.gz {1}".format(site.name, site.path))
                backup = copy("/tmp/{0}.tar.gz").format(site.name)[0]
            with new_site.platform.server:
                copy(backup)
                run("cd {1}; tar -zxf /tmp/{0}.tar.gz".format(site.path, site.name))

        with site.platform.server:
            # Generate the new site.
            self.generate_site(new_site)
    
    def migrate(self, site):

    def remove(self, site):
        

    def generate_site(self, site):
        site.path = "{0}/sites/{1}".format(site.platform.path, site.name)
        run("mkdir -p {0}".format(site.path))


        file_dirs = ["files", "private", "private/files", "private/tmp"]
        for file_dir in file_dirs:
            run("mkdir -p {0}/{1}".format(site.path, file_dir))
            run("chown {0}:{1} {2}/{3}".format(user, web_user, site.path, file_dir))


    def generate_settings_file(env, site):
        settings_template = env.get_template("settings.php")
        result = settings_template.render(database=site.database, extra=site.extra, conf=site.conf)

    def install_site(site, profile):
        local("drush @site si profile")
