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

    def is_table(self, table_name, record_format):
        existing_table_names = self.get_table_names()
        if table_name not in existing_table_names:
            return False
        record_format_keys = [pair[0] for pair in record_format]  
        record_format_key_types = [pair[1] for pair in record_format]  
        table_attributes = self.get_attributes(table_name)
        table_attribute_types = self.get_attribute_types(table_name=table_name, add_primary_key_flag=True)
        return record_format_keys == table_attributes and record_format_key_types == table_attribute_types

    def get_attributes(self, table_name):
        table_info = self.db.execute('PRAGMA table_info(' + ff.format_table_name(table_name) + ')', "fetch")
        attributes = [attribute_info[1] for attribute_info in table_info]
        return attributes

    def get_attribute_types(self, table_name, add_primary_key_flag=False):
        table_info = self.db.execute('PRAGMA table_info(' + ff.format_table_name(table_name) + ')', "fetch")
        attribute_types = [attribute_info[2] for attribute_info in table_info]
        if add_primary_key_flag:
            for i, attribute_info in enumerate(table_info):
                if attribute_info[5] == 1:
                    attribute_types[i] += " PRIMARY KEY"
                    break
        return attribute_types

    def get_primary_attribute(self, table_name):
        table_info = self.db.execute('PRAGMA table_info(' + ff.format_table_name(table_name) + ')', "fetch")
        for i, attribute_info in enumerate(table_info):
            if attribute_info[5] == 1:
                return attribute_info[1]

    def get_primary_attribute_position(self, table_name):
        table_info = self.db.execute('PRAGMA table_info(' + ff.format_table_name(table_name) + ')', "fetch")
        for i, attribute_info in enumerate(table_info):
            if attribute_info[5] == 1:
                return i

    def create_table(self, table_name, record_format, records=[], overwrite=False):
        if self.is_table(table_name, record_format) and not overwrite:
            return
        self.drop_table(table_name)
        table_structure = ", ".join([ff.format_attribute(pair[0]) + " " + pair[1] for pair in record_format])
        create_table_cmd = "CREATE TABLE " + ff.format_table_name(table_name) + "(" + table_structure + ")"
        self.db.execute(create_table_cmd, "commit")
        self.__insert_records(table_name, records)

    def drop_table(self, table_name):
        drop_table_cmd = "DROP TABLE if exists " + ff.format_table_name(table_name)
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
        insert_record_cmd = "INSERT INTO " + ff.format_table_name(table_name) + " VALUES(" + ", ".join(record_values) + ")"
        self.db.execute(insert_record_cmd, "commit")

    def __insert_records(self, table_name, records):
        if not records:
            return
        insert_records_cmd = "INSERT INTO " + ff.format_table_name(table_name) + " VALUES(" + ",".join(["?" for i in range(0, len(records[0]))]) + ")"
        self.db.execute(insert_records_cmd, "commit_many", records)

    def delete_record(self, table_name, condition):
        delete_record_cmd = "DELETE FROM " + ff.format_table_name(table_name) + " " + ff.format_condition(condition)

    def update_values(self, table_name, value, condition=None, attributes=all):
        update_value_cmd = "UPDATE " + ff.format_table_name(table_name) + " SET (" + ff.format_attributes(attributes) + ") = " + ff.format_value(value) + " " + ff.format_condition(condition)
        self.db.execute(update_value_cmd, "commit")

    def select_values(self, table_name, condition=None, attributes=all, order_attributes=None, order_type=""):
        attributes = ff.format_attributes(attributes)
        table_name = ff.format_table_name(table_name)
        condition = ff.format_condition(condition)
        order = ff.format_order(order_attributes, order_type)
        select_cmd = "SELECT " + attributes + " FROM " + table_name + " " + condition + " " + order
        data = self.db.execute(select_cmd, "fetch")
        return data

    def replace_data(self, table_name, data_old, data_new, attributes=all):
        record_values = [ff.format_value(value) for value in record]
        replace_data_cmd = "REPLACE INTO " + ff.format_table_name(table_name) + "(" + ff.format_attributes(attributes) + ") VALUES(" + ff.format_values([data_old, data_new]) + ")"
        self.db.execute(replace_data_cmd, "commit")

    def get_table(self, table_name):
        return self.select_values(table_name)

    def count_attributes(self, table_name):
        return len(self.get_attributes(table_name))

    def count_records(self, table_name):
        records = self.select_values(table_name)
        return len(records)
