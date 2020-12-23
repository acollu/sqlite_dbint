from sqlite_dbint import SqliteDatabaseInterface


db = SqliteDatabaseInterface("test.db")

db.create_table("trial", [("id", "integer PRIMARY KEY"), ("name", "text")])
#db.drop_table("trial")
record = (1, "JOHN")
db.insert_record("trial", record)
record = (2, "ADAM")
db.insert_record("trial", record)
#db.select_values("trial", ["id", "=", "1"], ["name"])
#db.update_field_value("trial", 1, "name", "ADAM")
#records = db.select_values("trial")
#print(db.is_table("trial"))
#print(db.count_records(records))
#db.drop_all_tables()
