"""
@file
Deploy, clone, backup and move sites
easily.
"""

from fabric.api import settings
#, abort, run, cd, sudo, put, env, prompt, get, open_shell

class Server:
    """
    A server has several services on it that can be used.
    """
    def __init__(self, hostname, user, port = 22, key=""):
        self.hostname = hostname
        self.user = user
        self.key = key
        self.port = port
        self.engines = {}

    def __enter__(self):
        hoststring = "{0}@{1}:{2}".format(self.user, self.hostname, self.port)
        self.con = settings(host_string=hoststring, port=self.port,
                            user=self.user, key_filename=self.key,
                            host=self.hostname, abort_on_prompts=True)
        return self.con.__enter__()

    def __exit__(self, type, value, traceback):
        return self.con.__exit__(type, value, traceback)

    def add_engine(self, engine):
        """
        Add a engine to this server, for instance a web server.
        """
        name = engine.engine_name
        if not self.engines.has_key(name):
            self.engines[name] = list()
        self.engines[name].append(engine)

    def get_engine(self, engine_name):
        """
        Look up and return engine(s) if we have any, else None.
        """
        if engine_name in self.engines.keys():
            return self.engines[engine_name]

    def verify_site(self, site):
        for engine_group in self.engines.values():
            for engine in engine_group:
                if engine.verify_site:
                    engine.verify_site(site)

    def verify_platform(self, platform):
        for engine_group in self.engines.values():
            for engine in engine_group:
                if engine.verify_site:
                    engine.verify_site(site)

class LocalServer(Server):
    """
    Localhost server, based on server.
    """
    def __init__(self):
        # FIXME: actually make me not use ssh to talk to myself.
        Server.__init__(self, "localhost", "badger", key="")

class Platform:
    """
    A platform is a code base that can host a number
    of sites on it.
    """
    def __init__(self, source_path, server):
        self.source_path = ""
        self.server = server

    def deploy(self, server, path):
        """
        Deploy a server on a specific path.
        """
        pass

    def verify(self):
        self.server.verify_platform(self)


    def verify_site(self, site):
        self.server.verify_site(site)

    def build(self):
        """
        Build this platform, for instance by running drush make,
        compiling less and sass and so on.
        """
        pass

class Site:
    """
    A site lives on a platform and has one or many
    database servers attached to it.
    """
    def __init__(self, name, platform, database_server):
        self.name = name
        self.platform = platform
        self.database_server = database_server

    def verify(self):
        self.database_server.verify_site(self)
        self.platform.verify_site(self)

    def clone(self, site):
        """
        Clone this site to another platform
        and potentially other database servers.
        """
        self.engine.clone(self, site)

    def migrate(self, new_platform, database_servers):
        """
        Migrate a site to a new platform.
        """
        pass

    def backup(self, backup_path):
        """
        Back the site up to a certain directory.
        """
        pass
