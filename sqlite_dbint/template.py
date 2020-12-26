from sqlite_database_interface import SqliteDatabaseInterface


db = SqliteDatabaseInterface("test.db")

db.drop_all_tables()
#db.drop_table("trial")

table_name = "trial one two"
record_format = [("id thing", "integer PRIMARY KEY"), ("name item", "text")]
db.create_table(table_name, record_format)
record = (1, "JOHN")
db.insert_record(table_name, record)
record = (2, "ADAM")
db.insert_record(table_name, record)
db.select_values(table_name, [("id thing", "=", 1)], ["name item"])
db.update_values(table_name, "ADAM", [("id thing", "=", 1)], ["name item"])
records = db.select_values(table_name)
print(db.is_table(table_name, record_format))
print(db.count_records(table_name))
