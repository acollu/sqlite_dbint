import sqlite3
from sqlite3 import Error
import sys

# Terminology:
# record: row
# attribute: column

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

    def is_table(self, table_name):
        existing_table_names = self.get_table_names()
        return table_name in existing_table_names

    def create_table(self, table_name, record_format, records=[], overwrite=False):
        if self.is_table(table_name) and not overwrite:
            return
        self.drop_table(table_name)
        table_structure = ", ".join([" ".join(pair) for pair in record_format])
        create_table_cmd = "CREATE TABLE " + table_name + "(" + table_structure + ")"
        self.execute(create_table_cmd, "commit")
        self.__insert_records(table_name, records)

    def drop_table(self, table_name):
        drop_table_cmd = "DROP TABLE if exists " + table_name
        self.execute(drop_table_cmd, "commit")

    def drop_all_tables(self):
        for table_name in self.get_table_names():
            self.drop_table(table_name)

    def is_record(self, table_name, unique_id_name, unique_id_value):
        unique_id_values = self.select_values(table_name=table_name, condition=None, attributes=[unique_id_name])
        unique_id_values = [value[0] for value in unique_id_values]
        return unique_id_value in unique_id_values

    def insert_record(self, table_name, record):
        record_values = [self.format_value(value) for value in record]
        insert_record_cmd = "INSERT INTO " + table_name + " VALUES(" + ", ".join(record_values) + ")"
        self.execute(insert_record_cmd, "commit")

    def __insert_records(self, table_name, records):
        insert_records_cmd = "INSERT INTO " + table_name + " VALUES(?, ?)"
        self.execute(insert_records_cmd, "commit_many", records)

    def delete_record(self, table_name, condition):
        delete_record_cmd = "DELETE FROM " + table_name + " " + self.format_condition(condition)

    def update_values(self, table_name, value, condition=None, attributes=all):
        update_value_cmd = "UPDATE " + table_name + " SET (" + self.format_attributes(attributes) + ") = " + self.format_value(value) + " " + self.format_condition(condition)
        self.execute(update_value_cmd, "commit")

    def select_values(self, table_name, condition=None, attributes=all):
        select_cmd = "SELECT " + self.format_attributes(attibutes) + " FROM " + table_name + " " + self.format_condition(condition)
        data = self.execute(select_cmd, "fetch")
        return data

    def replace_data(self, table_name, data_old, data_new, condition=None, attributes=all):
        record_values = [self.format_value(value) for value in record]
        replace_data_cmd = "REPLACE INTO " + table_name + "(" + self.format_attributes(attributes) ") VALUES(" + self.format_values([data_old, data_new]) + ")"
        self.execute(replace_data_cmd, "commit")

    def get_table_names(self):
        table_names = self.execute('SELECT name FROM sqlite_master where type = "table"', "fetch")
        table_names = [str(table_name[0]) for table_name in table_names]
        return table_names

    def get_table(self, table_name):
        return self.select_values(table_name)

    def count_records(self, records):
        return len(records)

    def format_attributes(self, attributes):
        if attributes==all:
            return "*"
        elif isinstance(attributes, list):
            return ", ".join(attributes)
        else:
            TypeError

    def format_value(self, value):
        if isinstance(value, int):
            return str(value)
        elif isinstance(value, str):
            return '"' + value + '"'
        else:
            raise TypeError

    def format_values(self, values):
        return ", ".join([self.format_value(value) for value in values])

    def format_condition(self, condition):
       if condition == None:
           return ""
       elif isinstance(condition, list):
           condition[-1] = self.format_record_value(condition[-1])
           return "where " + " ".join(condition)
       else:
           raise TypeError
