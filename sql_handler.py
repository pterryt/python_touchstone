""" This is the class for the database object pythonized """
import re
import database

def create_dbs_from_sqldump(filepath: str):
    db = database.Database()
    current_table = None
    data_pattern = re.compile(r"INSERT INTO `\w+` VALUES \((.+)\)")
    column_pattern = re.compile(r"`(\w+)`\s+(\w+)")

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("CREATE TABLE"):
                current_table = database.DatabaseTable()
                current_table.name = re.search(r"`(\w+)`", line).group(1)

            elif current_table and line.startswith("`"):
                match = column_pattern.search(line)
                column_name = match.group(1)
                column_type = match.group(2)
                current_table.add_column(column_name, column_type)

            elif data_match := data_pattern.match(line):
                values = data_match.group(1)
                rows = [row.split(",") for row in re.findall(r"\((.*?)\)", values)]
                current_table.add_rows(rows)
                db.add_table(current_table.name, current_table)
                current_table = None

    return db


# file_path = "sql_dumps/EnglishLocale.sql"
# parsed_data = create_dbs_from_sqldump(file_path)
#
# for db in parsed_data:
#     db.print_details()
