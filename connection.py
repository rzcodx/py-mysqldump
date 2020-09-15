import mysql.connector
import getpass
from mysql.connector import Error


class Connection:
    host = None
    user = None
    password = None
    connection = None

    def __init__(self):
        host = input("Host (localhost): ")
        self.host = "localhost" if host == "" else host

        user = input("User (admin): ")
        self.user = "admin" if user == "" else user

        password = getpass.getpass("Password (admin): ")
        self.password = "admin" if password == "" else password

        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        except Error as e:
            print(e)
            exit()

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor
