import sys
from .sqlite3_interface import Sqlite3Interface
from .field_formatter import FieldFormatter as ff

# Terminology:
# record: row
# attribute: column

class SqliteDatabaseInterface:
    def __init__(self, database_name):
        self.db = Sqlite3Interface(database_name)

    def __del__(self):
        del self.db

    def get_table_names(self):
        table_names = self.db.execute('SELECT name FROM sqlite_master where type = "table"', "fetch")
        table_names = [str(table_name[0]) for table_name in table_names]
        return table_names

    def is_table(self, table_name):
        existing_table_names = self.get_table_names()
        return table_name in existing_table_names

    def create_table(self, table_name, record_format, records=[], overwrite=False):
        if self.is_table(table_name) and not overwrite:
            return
        self.drop_table(table_name)
        table_structure = ", ".join([" ".join(pair) for pair in record_format])
        create_table_cmd = "CREATE TABLE " + table_name + "(" + table_structure + ")"
        self.db.execute(create_table_cmd, "commit")
        self.__insert_records(table_name, records)

    def drop_table(self, table_name):
        drop_table_cmd = "DROP TABLE if exists " + table_name
        self.db.execute(drop_table_cmd, "commit")

    def drop_all_tables(self):
        for table_name in self.get_table_names():
            self.drop_table(table_name)

    def is_record(self, table_name, unique_id_name, unique_id_value):
        unique_id_values = self.select_values(table_name=table_name, condition=None, attributes=[unique_id_name])
        unique_id_values = [value[0] for value in unique_id_values]
        return unique_id_value in unique_id_values

    def insert_record(self, table_name, record):
        record_values = [ff.format_value(value) for value in record]
        insert_record_cmd = "INSERT INTO " + table_name + " VALUES(" + ", ".join(record_values) + ")"
        self.db.execute(insert_record_cmd, "commit")

    def __insert_records(self, table_name, records):
        insert_records_cmd = "INSERT INTO " + table_name + " VALUES(?, ?)"
        self.db.execute(insert_records_cmd, "commit_many", records)

    def delete_record(self, table_name, condition):
        delete_record_cmd = "DELETE FROM " + table_name + " " + ff.format_condition(condition)

    def update_values(self, table_name, value, condition=None, attributes=all):
        update_value_cmd = "UPDATE " + table_name + " SET (" + ff.format_attributes(attributes) + ") = " + ff.format_value(value) + " " + ff.format_condition(condition)
        self.db.execute(update_value_cmd, "commit")

    def select_values(self, table_name, condition=None, attributes=all, order_attributes=None, order_type=""):
        attributes = ff.format_attributes(attributes)
        condition = ff.format_condition(condition)
        order = ff.format_order(order_attributes, order_type)
        select_cmd = "SELECT " + attributes + " FROM " + table_name + " " + condition + " " + order
        data = self.db.execute(select_cmd, "fetch")
        return data

    def replace_data(self, table_name, data_old, data_new, attributes=all):
        record_values = [ff.format_value(value) for value in record]
        replace_data_cmd = "REPLACE INTO " + table_name + "(" + ff.format_attributes(attributes) + ") VALUES(" + ff.format_values([data_old, data_new]) + ")"
        self.db.execute(replace_data_cmd, "commit")

    def get_table(self, table_name):
        return self.select_values(table_name)

    def count_records(self, table_name):
        records = self.select_values(table_name)
        return len(records)
