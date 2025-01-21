from database import DatabaseTable, Database
import xliff_handler
import string_utils
import hash
import sql_handler as sh

enCode = 1
cnCode = 5

def remove_stringless(db: Database) -> None:
    for table in db.tables:
        if isinstance(table, DatabaseTable):
            if not table.does_type_exist("text"):
                db.remove_table(table.name)

def chinese_strings_in_data(column_data:list[str]) -> bool:
    for data_string in column_data:
        if string_utils.contains_hanzi(data_string):
            return True
    return False

def get_non_matching_strings(eng_list:list[str], cn_list:list[str]) -> None | list[str]:
    print(f"Length of English List: {eng_list}")
    print(f"Length of Chinese List: {cn_list}")
    return_list = list()
    for index, locale_string in enumerate(cn_list):
        if not locale_string == eng_list[index]:
            return_list.append(locale_string)
    return return_list if not len(return_list) == 0 else None


def get_strings_to_localize(eng_db: Database, cn_db: Database) -> None | list[dict]:
    print("Getting localized strings...")
    # remove_stringless(eng_db)
    # remove_stringless(cn_db)
    return_list = list()
    for index, table in enumerate(cn_db.tables):
        eng_table = eng_db.tables[index]
        print(f"EnglishTable ObjectType: {type(eng_table)}")
        print(f"ChineseTable ObjectType: {type(table)}")
        if isinstance(table, DatabaseTable) and isinstance(eng_table, DatabaseTable):
            column_names = table.get_column_names()
            for column_name in column_names:
                print(f"Column_Name: {column_name}")
                cn_index, data = table.get_column(column_name)
                if cn_index >= 0 and chinese_strings_in_data(data):
                    if column_name.endswith("5"):
                        trimmed_name = column_name[:-1]
                        eng_column_equivalent = trimmed_name + "1"
                        eng_index, eng_data = eng_table.get_column(eng_column_equivalent)
                        if eng_index >= 0:
                            nm_strings = get_non_matching_strings(eng_data, data)
                            print(nm_strings)
                            if nm_strings:
                                return_list.append({"name": trimmed_name, "data": eng_data, "file": eng_db.source_file})
    return return_list if not len(return_list) == 0 else None


eng_file_path = "sql_dumps/EnglishLocale.sql"
cn_file_path = "sql_dumps/ChineseLocale.sql"
eng_database = sh.create_db_from_sqldump(eng_file_path)
cn_database = sh.create_db_from_sqldump(cn_file_path)
eng_database.dump_db()
cn_database.dump_db()

stl = get_strings_to_localize(eng_database, cn_database)
# print(len(stl))
# print(stl[0])