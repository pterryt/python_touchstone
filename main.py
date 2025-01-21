import data_filter
import sql_handler

# main entry point for the program.
# check 'en_json' and 'cn_json' directories for the input files
# check 'output' directory for the xliff output
def main():

    # load the databases into memory
    enUS_db, zhCN_db = sql_handler.test_fuction()
    # filter the data
    xliff_files = data_filter.get_strings_to_localize(enUS_db, zhCN_db)
    # write them to file
    for file in xliff_files:
        file.write_to_file()


if __name__ == "__main__":
    main()