import os

from connection import Connection


class ImportDB:
    directory = None
    connection = None

    def __init__(self):
        directory = input("Directory (backup): ")
        self.directory = "backup" if directory == "" else directory
        self.connection = Connection()

    def database_exist(self, database_name):
        query = f"SHOW DATABASES LIKE '{database_name}'"
        database = self.connection.execute(query).fetchone()
        return False if database is None else True

    def create_db(self, database_name):
        query = f"CREATE DATABASE {database_name} CHARACTER SET 'UTF8' COLLATE 'utf8_general_ci';"
        self.connection.execute(query)
        return database_name

    def import_db_from_file(self, database_name, path):
        try:
            if self.database_exist(database_name):
                return False

            self.create_db(database_name)

            os.system(
                f"mysql -u{self.connection.user} -p{self.connection.password} --skip-comments {database_name} < '{path}' 2> null")
            print(f"{path} imported.")
        except NameError as e:
            print(f"Error importing {path}. Message: {e}")

    def is_valid_file(self, extension):
        return True if extension == '.sql' else False

    def import_database(self, file):
        path = os.path.join(self.directory, file)
        if not os.path.isfile(path):
            return False

        name, extension = os.path.splitext(file)
        if not self.is_valid_file(extension):
            return False

        return True

    def init(self):
        resp = input(f"Import all databases? y/n (Default n): ")
        all_databases = True if resp == 'y' else False

        files = os.listdir(self.directory)

        for file in files:
            path = os.path.join(self.directory, file)
            name, extension = os.path.splitext(file)

            if not self.import_database(file):
                continue

            if all_databases:
                self.import_db_from_file(name, path)
                continue

            resp = input(f"Import {path}? y/n (Default y): ")
            resp = False if resp == "n" else True
            if resp:
                self.import_db_from_file(name, path)

        exit()


import_db = ImportDB()
import_db.init()
