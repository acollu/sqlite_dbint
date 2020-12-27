from .sqlite_database_interface import SqliteDatabaseInterface

class SqliteDatabaseDisplay:
    def __init__(self, database_name):
        self.db = SqliteDatabaseInterface(database_name)

    def __del__(self):
        self.db

    def list_table_names(self):
        table_names = self.db.get_table_names()
        print("Database - table report")
        print("Table name: number of records")
        for table_name in table_names:
            number_of_records = self.db.count_records(table_name)
            print(table_name, ": ", str(number_of_records))

    def display_table(self, table_name, cell_width=20):
        primary_attribute_position = self.db.get_primary_attribute_position(table_name)
        primary_attribute = self.db.get_primary_attribute(table_name)
        other_attributes = [attribute for attribute in self.db.get_attributes(table_name) if attribute != primary_attribute]
        self.print_horizontal_delimiter(table_name, cell_width)
        self.print_info_line([primary_attribute, *other_attributes], cell_width)
        self.print_horizontal_delimiter(table_name, cell_width)
        for record in self.db.select_values(table_name):
            record = list(record)
            primary_attribute_value = record[primary_attribute_position]
            del record[primary_attribute_position]
            self.print_info_line([primary_attribute_value, *record], cell_width)
            self.print_horizontal_delimiter(table_name, cell_width)

    def print_horizontal_delimiter(self, table_name, cell_width):
        line = "-" + "-".join(["-"*cell_width for i in range(0, self.db.count_attributes(table_name))]) + "-"
        print(line)

    def print_info_line(self, record, cell_width):
        line = "|"
        for value in record:
            line += (value if isinstance(value, str) else str(value)).ljust(cell_width, " ")
            line += "|"
        print(line)

#display = SqliteDatabaseDisplay("test.db")
#display.list_table_names()
#display.display_table(table_name="trial", cell_width=30)
