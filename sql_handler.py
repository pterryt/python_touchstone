""" This is the class for the database object pythonized """
from database import DatabaseTable, Database
import json
import os

# function that takes a list of names (the database files we want to ingest)
# and convert the data to a database object so we can create our own function for dealing with the data
def create_db_from_json(dir_path:str, db_list:list) -> Database:
    db = Database()

    for db_file in db_list:
        db_file_name = db_file + ".json"
        filepath = os.path.join(dir_path, db_file_name)
        with open(filepath, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            # just how data is broken into tables in SQL, and in our JSON files, our database objects
            # contain a list of database tables that represent those structures
            table = DatabaseTable()
            table.name = db_file
            # json files already have as scheme section suitable for our needs, we can store it directly in our object
            table.schema = json_data.get('schema', {})
            # same goes for data
            table.data = json_data.get('data', {})
            db.add_table(table)
    return db


# this function was used for testing the program throughout developement and in the final test in __main__
# it loads the test jsons and returns the database objects we'll be using
def test_fuction():
    files = ["faction", "chartitles", "areagroup"]
    en_db = create_db_from_json("en_json", files)
    cn_db = create_db_from_json("cn_json", files)
    return en_db, cn_db
