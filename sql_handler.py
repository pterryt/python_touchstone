""" This is the class for the database object pythonized """
from database import DatabaseTable, Database
import json
import os

def create_db_from_json(dir_path:str, db_list:list) -> Database:
    db = Database()

    for db_file in db_list:
        db_file_name = db_file + ".json"
        filepath = os.path.join(dir_path, db_file_name)
        with open(filepath, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            table = DatabaseTable()
            table.name = db_file
            table.schema = json_data.get('schema', {})
            table.data = json_data.get('data', {})
            db.add_table(table)
    return db





files = ["faction", "chartitles", "areagroup"]
en_db = create_db_from_json("en_json", files)
cn_db = create_db_from_json("cn_json", files)

for tb in en_db.tables:
    if isinstance(tb, DatabaseTable):
        tb.print_details()

# with open("db_test.txt", "w") as f:

#
# for index,db in enumerate(parsed_data.tables):
#     print(index)
#     db["table"].print_details()
