import mysql.connector


class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'aa11632LX1$'
        self.database = 'SmartDeviceManagement'

    def create_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
