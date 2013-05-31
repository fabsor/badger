import unittest
import MySQLdb as mdb
import mocks
import sys
from mocks import MockEngine
from settings import mysql
from badger.mysql import MysqlEngine
from badger.types import Site, Server, Platform


class MysqlEngineTest(unittest.TestCase):
    """
    Test mysql engine. This requires a mysql server.
    """
    def testVerifySite(self):
        """
        Create a sample database for a site.
        """
        # Set up a mock engine for the platforms
        mocked_engine = MockEngine()
        # Set up the mysql engine.
        db_engine = MysqlEngine(mysql["host"], mysql["user"], mysql["password"])
        server = Server("127.0.0.1", "deployer")
        server.add_engine(mocked_engine)
        server.add_engine(db_engine)

        platform = Platform("./testplatform", server)
        site = Site("example_.com", platform, server)
        site.verify()
        self.assertTrue(self.databaseExists("examplecom"), "Database exists")
        self.assertTrue(self.userExists("examplecom", "127.0.0.1"), "User exists")
        self.assertTrue(self.connectionWorks(site), "Connection works")

    def userExists(self, user, host):
        db = mdb.connect("127.0.0.1", "root", "", "mysql")
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT count(User) FROM user WHERE User = %s and Host = %s",
            (user, host))
            return cursor.fetchone()[0] == 1

    def databaseExists(self, database):
        db = mdb.connect("127.0.0.1", "root", "")
        with db:
            cursor = db.cursor()
            cursor.execute("SHOW DATABASES")
            for row in cursor.fetchall():
                if row[0] == database:
                    return True
            return False

    def connectionWorks(self, site):
        try:
            test_con = mdb.connect(site.database["host"], site.database["user"], site.database["password"], site.database["name"])
            return True
        except Exception:
            return False

    def tearDown(self):
        db = mdb.connect("127.0.0.1", "root", "", "mysql")
        with db:
            cursor = db.cursor()
            cursor.execute("DROP DATABASE examplecom")
            cursor.execute("DROP USER %s@%s", ("examplecom", mysql["host"]))
