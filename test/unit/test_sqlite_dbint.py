from sqlite_dbint import SqliteDatabase


db = SqliteDatabase("test.db")

db.create_table("trial", {"id": "integer PRIMARY KEY", "name": "text"})
#db.recreate_table("trial", {"id": "integer PRIMARY KEY", "name": "text"})
#db.drop_table("trial")
entry = {"id": 1, "name": "JOHN"}
db.insert_entry("trial", entry)
entry = {"id": 2, "name": "ADAM"}
db.insert_entry("trial", entry)
db.select_fields("trial", ["id", "=", "1"], ["name"])
#db.update_field_value("trial", 1, "name", "ADAM")
entries = db.select_fields("trial")
#print(db.is_table("trial"))
print(db.count_entries(entries))
db.drop_all_tables()


