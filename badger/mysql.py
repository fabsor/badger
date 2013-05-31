import MySQLdb as mdb

class MysqlEngine:
    """
    Create databases and users and manage cloning and dumping of
    databases.
    """
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def create_connection(self, database=""):
        return mdb.connect(host=self.host, user=self.user, passwd=self.password, db=database)
        

    def verify_site(self, site):
        if not hasattr(site, "database"):
            site.database = {}
        if not "name" in site.database:
            site.database["name"] = site.name.replace(".", "").lower()
        if not "password" in site.database:
            site.database["password"] = "password" # Todo: generate password properly.
        if not "user" in site.database:
            site.database["user"] = site.database["name"]
        if not "host" in site.database:
            site.database["host"] = site.platform.server.hostname

        self.create_database(site.database["name"])
        self.create_user(site.database["name"], site.database["password"])
        self.grant_privileges(site.database["name"], site.database["user"], site.database["host"], site.database["password"])

    def create_database(self, name):
        db = self.create_connection()
        with db:
            cursor = db.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(name))

    def create_user(self, name, password):
        db = self.create_connection("mysql")
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT count(User) FROM user WHERE User = %s", (name))
            if cursor.fetchone() == 0:
                cursor.execute("CREATE USER {0} IDENTIFIED BY '{1}'".format(name, password))
    
    def grant_privileges(self, database, username, host, password):
        db = self.create_connection()
        with db:
            cursor = db.cursor()
            cursor.execute("GRANT ALL PRIVILEGES ON {0}.* TO '{1}'@'{2}' IDENTIFIED BY '{3}'".format(database, username, host, password))

    def close_conection(self):
        self.db.close()
