import sqlite3



class Database:
    def __init__(self):
        self._database_name = "tasks.db"
        self._table_name = "TASKS"
        self._column_id = "ID"
        self._column_task = "TASK"
        self.create_table()

    def create_table(self, is_temp=""):
        with self._get_database(self._database_name) as database:
            cursor = database.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {is_temp}{self._table_name} ("
                           f"{self._column_id} INTEGER PRIMARY KEY, "
                           f"{self._column_task} TEXT, "
                           f"UNIQUE({self._column_id}, {self._column_task})"
                           f")")

    def get_tasks(self, is_temp=""):
        with self._get_database(self._database_name) as database:
            cursor = database.cursor()
            tasks = cursor.execute(f"SELECT * FROM {is_temp}{self._table_name}").fetchall()
        return tasks

    def _get_database(self, database_name):
        return sqlite3.connect(database_name)

    def insert(self, row_id, text, is_temp=""):
        with self._get_database(self._database_name) as database:
            cursor = database.cursor()
            cursor.execute(f"INSERT INTO {is_temp}{self._table_name} ({self._column_id}, {self._column_task}) VALUES(?, ?)", [row_id, text])

    def replace(self, row_id, text):
        pass

    def delete(self, row_id, text, is_temp=""):
        with self._get_database(self._database_name) as database:
            cursor = database.cursor()
            cursor.execute(f"DELETE FROM {is_temp}{self._table_name} WHERE ({self._column_id}, {self._column_task}) = (?, ?)", [row_id, text])

    def delete_all(self, is_temp=""):
        with self._get_database(self._database_name) as database:
            cursor = database.cursor()
            cursor.execute(f"DELETE FROM {is_temp}{self._table_name}")

    def copy_from_temp(self):
        with self._get_database(self._database_name) as database:
            cursor = database.cursor()
            cursor.execute(f"INSERT INTO {self._table_name} SELECT * FROM temp{self._table_name}")