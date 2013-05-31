"""
@file
Deploy, clone, backup and move sites
easily.
"""

class Server:
    """
    A server has several services on it that can be used.
    """
    def __init__(self, hostname, user, key=""):
        self.hostname = hostname
        self.user = user
        self.key = key
        self.engines = []

    def add_engine(self, engine):
        """
        Add a engine to this server, for instance a web server.
        """
        self.engines.append(engine)

    def verify_site(self, site):
        for engine in self.engines:
            if engine.verify_site:
                engine.verify_site(site)
            
    def verify_platform(self, platform):
        for engine in self.engines:
            if engine.verify_site:
                engine.verify_site(site)

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

    def verify(self):
        self.server.verify_platform(self)


    def verify_site(self, site):
        self.server.verify_site(site)

    def build(self):
        """
        Build this platform, for instance by running drush make,
        compiling less and sass and so on.
        """

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

    def backup(self, backup_path):
        """
        Back the site up to a certain directory.
        """

class DatabaseEngine:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

