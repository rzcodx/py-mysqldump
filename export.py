import os

from connection import Connection


class Export:
    directory = None
    connection = None

    def __init__(self):
        directory = input("Directory (backup): ")
        self.directory = "backup" if directory == "" else directory
        self.connection = Connection()

    def export(self, database_name):
        try:
            if not os.path.exists(self.directory):
                os.mkdir(self.directory)

            os.system(
                f"mysqldump -u{self.connection.user} -p{self.connection.password} --skip-comments {database_name} > '{self.directory}/{database_name}.sql' 2> null")
            print(f"{database_name} exported.")
        except NameError as e:
            print(f"Error exporting {database_name}. Message: {e}")

    def init(self):
        query = "SHOW DATABASES"
        databases = self.connection.execute(query).fetchall()

        resp = input(f"Export all databases? y/n (Default n): ")
        all_databases = True if resp == 'y' else False

        for item in databases:
            database_name = item[0]

            if all_databases:
                self.export(database_name)
                continue

            resp = input(f"Export {database_name}? y/n (Default y): ")
            resp = False if resp == "n" else True
            if resp:
                self.export(database_name)

        exit()


export = Export()
export.init()
