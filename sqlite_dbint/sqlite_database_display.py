from .sqlite_database_interface import SqliteDatabaseInterface

class SqliteDatabaseDisplay:
    def __init__(self, database_name):
        self.db = SqliteDatabaseInterface(database_name)
        self.char_per_attribute = 10

    def __del__(self):
        self.db

    def list_table_names(self):
        table_names = self.db.get_table_names()
        for table_name in table_names:
            number_of_records = self.db.count_records(table_name)
            print(table_name, ": ", str(number_of_records))

    def display_table(self, table_name):
        primary_attribute_position = self.db.get_primary_attribute_position(table_name)
        primary_attribute = self.db.get_primary_attribute(table_name)
        other_attributes = [attribute for attribute in self.db.get_attributes(table_name) if attribute != primary_attribute]
        self.print_horizontal_delimiter(table_name)
        self.print_info_line([primary_attribute, *other_attributes])
        self.print_horizontal_delimiter(table_name)
        for record in self.db.select_values(table_name):
            record = list(record)
            primary_attribute_value = record[primary_attribute_position]
            del record[primary_attribute_position]
            self.print_info_line([primary_attribute_value, *record])
            self.print_horizontal_delimiter(table_name)

    def print_horizontal_delimiter(self, table_name):
        line = "-" + "-".join(["-"*self.char_per_attribute for i in range(0, self.db.count_records(table_name))]) + "-"
        print(line)

    def print_info_line(self, record):
        line = "|"
        for value in record:
            line += (value if isinstance(value, str) else str(value)).ljust(self.char_per_attribute, " ")
            line += "|"
        print(line)

display = SqliteDatabaseDisplay("test.db")
display.list_table_names()
display.display_table("trial")
