from database import DatabaseTable, Database
import xliff_handler
import string_utils

# based on the data from the original api
# each table containing locale information in the database has a int mask depending on the language
# since the English mask is 1 and the Chinese is 5
# we will use these numbers where necessary for comparing the two sets of data
enCode = "1"
cnCode = "5"


# check if a column name has Chinese locale information based on the mask
def chinese_locale_column(column_name:str) -> bool:
    return column_name.endswith(cnCode) and not column_name.endswith("15")

# function for making sure we skip over databases without string data
def remove_stringless(db: Database) -> None:
    for table in db.tables:
        if isinstance(table, DatabaseTable):
            if not table.does_type_exist("text"):
                db.remove_table(table.name)

# checks a column to see if there are any Chinese characters in the content
# returns as soon as it finds any as we know this will be a column of interest
def chinese_strings_in_data(column_data:list[str]) -> bool:
    for data_string in column_data:
        if string_utils.contains_hanzi(data_string):
            return True
    return False

# simple string comparison of the data for two columns
# used to compare the English to the Chinese
# the reason being is if the strings were not translated, the original translators did not translate that string
# and it likely is never seen by the users. Since we don't want to waste time translating strings that are never seen,
# we reduce to the list to only translated strings
def get_non_matching_strings(eng_list:list[str], cn_list:list[str]) -> None | list[str]:
    return_list = list()
    # enumerate is used often as we need to use the index to compare the two locales often
    # since the data was ingested in the same way for both databases, the indexes should always line up
    for index, locale_string in enumerate(cn_list):
        if not locale_string == eng_list[index]:
            return_list.append(locale_string)
    return return_list


def get_strings_to_localize(eng_db: Database, cn_db: Database) -> None | list[xliff_handler.XliffFile]:
    print("Getting localized strings...")
    # remove stringless tables immediately so there is no unnecessary processing
    remove_stringless(eng_db)
    remove_stringless(cn_db)
    return_list = list()
    for index, cn_table in enumerate(cn_db.tables):
        eng_table = eng_db.tables[index]
        # type check to be sure are infact dealing with DatabaseTables
        # mostly because my IDE refused to do symbol suggestions otherwise
        if isinstance(cn_table, DatabaseTable) and isinstance(eng_table, DatabaseTable):
            text_columns = list()
            eng_text_columns = list()
            locale_columns = list()
            # store the names of the relevant tables - ones that are Chinese text
            for c_index, column in enumerate(cn_table.schema):
                if column["Type"] == "text" and chinese_locale_column(column["Field"]):
                    text_columns.append(column["Field"])
                    # get the English name is as simple as swapping the int mask
                    eng_text_columns.append(column["Field"][:-1] + enCode)
            # get the column data with the names we collected
            for d_index, column in enumerate(text_columns):
                rt1, cn_column = cn_table.get_column(column)
                rt2, eng_column = eng_table.get_column(eng_text_columns[index])
                # the first value in the return tuple from get_column
                # is True or False depending on if the given column exists
                # if the column is not found in either table we do not proceed
                if rt1 and rt2:
                    nm_strings = get_non_matching_strings(cn_column, eng_column)
                    # make xliff entries for each of the strings that were localized into Chinese
                    for string in nm_strings:
                        new_xliff_object = xliff_handler.XliffEntry(string)
                        locale_columns.append(new_xliff_object)
            if locale_columns:
                # put the entries into a xliff file object and add it to the return list
                new_xliff_file = xliff_handler.XliffFile(cn_table.name, locale_columns)
                return_list.append(new_xliff_file)
    return return_list