import sqlite3
from sqlite3 import Error

class Sqlite3Interface:
    def __init__(self, database_name):
        self.connection = self.connect(database_name)

    def __del__(self):
        self.connection.close()

    def connect(self, database_name):
        try:
            connection = sqlite3.connect(database_name)
            return connection
        except Error:
            print(Error)
            sys.exit()

    def execute(self, cmd, cmd_type='read', data=None):
        cursor = self.connection.cursor()
        if cmd_type == "commit":
            print(cmd)
            cursor.execute(cmd)
            self.connection.commit()
        elif cmd_type == "commit_many" and data is not None:
            print(cmd)
            cursor.executemany(cmd, data)
            self.connection.commit()
        elif cmd_type == "fetch":
            print(cmd)
            cursor.execute(cmd)
            data = cursor.fetchall()
            return data
        else:
            raise TypeError
