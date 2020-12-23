import sqlite3
from sqlite3 import Error
import sys

class SqliteDatabaseInterface:
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

    def execute(self, cmd, cmd_type='read'):
        cursor = self.connection.cursor()
        if cmd_type == "commit":
            print(cmd)
            cursor.execute(cmd)
            self.connection.commit()
        elif cmd_type == "fetch":
            print(cmd)
            cursor.execute(cmd)
            data = cursor.fetchall()
            return data
        else:
            raise TypeError

    def create_table(self, table_name, entry_format):
        table_structure = ", ".join([" ".join(pair) for pair in zip(entry_format.keys(), entry_format.values())])
        create_table_cmd = "CREATE TABLE if not exists " + table_name + "(" + table_structure + ")"
        self.execute(create_table_cmd, "commit")

    def drop_table(self, table_name):
        drop_table_cmd = "DROP TABLE if exists " + table_name
        self.execute(drop_table_cmd, "commit")

    def drop_all_tables(self):
        for table_name in self.get_table_names():
            self.drop_table(table_name)

    def recreate_table(self, table_name, entry_format):
        self.drop_table(table_name)
        self.create_table(table_name, entry_format)

    def insert_entry(self, table_name, entry):
        entry_values = [self.format_field_value(value) for value in entry.values()]
        insert_entry_cmd = "INSERT INTO " + table_name + " VALUES(" + ", ".join(entry_values) + ")"
        self.execute(insert_entry_cmd, "commit")

    def delete_entry(self, table_name, condition):
        delete_entry_cmd = "DELETE FROM " + table_name + " " + self.format_condition(condition)

    def update_field_value(self, table_name, condition, field_key, field_value):
        update_field_value_cmd = "UPDATE " + table_name + " SET " + field_key + " = " + self.format_field_value(field_value) + " " + self.format_condition(condition)
        self.execute(update_field_value_cmd, "commit")

    def select_fields(self, table_name, condition=None, field_keys=all):
        select_cmd = "SELECT " + self.format_field_keys(field_keys) + " FROM " + table_name + " " + self.format_condition(condition)
        data = self.execute(select_cmd, "fetch")
        return data

    def get_table_names(self):
        table_names = self.execute('SELECT name from sqlite_master where type = "table"', "fetch")
        table_names = [str(table_name[0]) for table_name in table_names]
        return table_names

    def get_table(self):
        return self.select_fields()

    def is_table(self, table_name):
        is_table_cmd = 'SELECT name from sqlite_master WHERE type = "table" AND name = ' + table_name
        is_table = self.execute(is_table_cmd, "fetch")
        return is_table

    def count_entries(self, entries):
        return len(entries)

    def format_field_keys(self, field_keys):
        if field_keys==all:
            return "*"
        elif isinstance(field_keys, list):
            return ", ".join(field_keys)
        else:
            TypeError

    def format_field_value(self, field_value):
        if isinstance(field_value, int):
            return str(field_value)
        elif isinstance(field_value, str):
            return '"' + field_value + '"'
        else:
            raise TypeError

    def format_condition(self, condition):
       if condition == None:
           return ""
       elif isinstance(condition, list):
           condition[-1] = self.format_field_value(condition[-1])
           return "where " + " ".join(condition)
       else:
           raise TypeError
