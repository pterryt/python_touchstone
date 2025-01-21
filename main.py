# import sql_handler as sh
import data_filter
import sql_handler
import xliff_handler

def main():
    # e, c = sh.test_fuction()
    # e(1)
    # print(e.tables[0].get_column("ID"))

    enUS_db, zhCN_db = sql_handler.test_fuction()
    xliff_files = data_filter.get_strings_to_localize(enUS_db, zhCN_db)
    for file in xliff_files:
        file.write_to_file()


if __name__ == "__main__":
    main()