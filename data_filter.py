from database import DatabaseTable, Database
import xliff_handler
import string_utils
import hash
import sql_handler as sh

enCode = 1
cnCode = 5

def chinese_locale_column(column_name:str) -> bool:
    return column_name.endswith("5") and not column_name.endswith("15")

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
    # print(f"Length of English List: {len(eng_list)}")
    # print(f"Length of Chinese List: {len(cn_list)}")
    return_list = list()
    for index, locale_string in enumerate(cn_list):
        if not locale_string == eng_list[index]:
            return_list.append(locale_string)
    # print(f"Length of return_list of get_non_matching_strings {len(return_list)}")
    return return_list


def get_strings_to_localize(eng_db: Database, cn_db: Database) -> None | list[dict]:
    print("Getting localized strings...")
    remove_stringless(eng_db)
    remove_stringless(cn_db)
    return_list = list()
    for index, cn_table in enumerate(cn_db.tables):
        eng_table = eng_db.tables[index]
        if isinstance(cn_table, DatabaseTable) and isinstance(eng_table, DatabaseTable):
            text_columns = list()
            eng_text_columns = list()
            locale_columns = list()
            for c_index, column in enumerate(cn_table.schema):
                if column["Type"] == "text" and chinese_locale_column(column["Field"]):
                    text_columns.append(column["Field"])
                    eng_text_columns.append(column["Field"][:-1] + "1")
            # print(f"Text Column: {text_columns}")
            # print(f"English Text Column: {eng_text_columns}")
            for d_index, column in enumerate(text_columns):
                rt1, cn_column = cn_table.get_column(column)
                rt2, eng_column = eng_table.get_column(eng_text_columns[index])
                if rt1 and rt2:
                    nm_strings = get_non_matching_strings(cn_column, eng_column)
                    for string in nm_strings:
                        new_dict = { "hash": hash.hash_string(string), "text": string }
                        locale_columns.append(new_dict)
            # print(len(locale_columns))
            if locale_columns:
                return_list.append({"table_name": cn_table.name, "source_strings": locale_columns})
    # print(f"Whaaa {len(return_list)}")
    return return_list


files = ["faction", "chartitles", "areagroup"]
e_db = sh.create_db_from_json("en_json", files)
c_db = sh.create_db_from_json("cn_json", files)

stl = get_strings_to_localize(e_db, c_db)
print(stl)