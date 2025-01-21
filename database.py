class DatabaseTable:
    def __init__(self):
        self.name = ""
        self.schema = list()
        self.data = list()

    # gets the column data from a table given a column name
    # returns True and the data, or False and None if the column name does not exist
    def get_column(self, column_name:str) -> tuple:
        for index, column in enumerate(self.schema):
            if column["Field"] == column_name:
                column_data = [row[column_name] for row in self.data]
                return True, column_data
        return False, None

    # same as the above but by index
    # function exists so we can iterate through the Chinese table
    # and access the English table equivalent simultaneously
    def get_column_by_index(self, index:int) -> tuple:
        found = False
        column_data = list()
        try:
            column_data.extend([row[index] for row in self.data])
            found = True
        except KeyError as e:
            print(f"Failed to get data from index = {index} : {e}")
        return found, column_data

    # get the column type given a column name
    # returns the index and type, or -1 and None if the column doesn't exist
    # we're mainly only intersted in text columns
    def get_column_type(self, column_name:str) -> tuple:
        for index, column in enumerate(self.schema):
            if column["Field"] == column_name:
                return index, column["Type"]
        return -1, None

    # used to reduce the bulk sum of data
    # since many tables lack any string at all, let's not process them further
    def does_type_exist(self, data_type:str) -> bool:
        for column in self.schema:
            if column["Type"] == data_type:
                return True
        return False

    # used for debugging
    # just prints out the table name, schema, and a bit of data to see what we're working with
    def print_details(self) -> None:
        print(f"""
        Database Name: {self.name}
        Database Schema: {self.schema}
        Data Sample(5): {self.data[:5]}
            """)

# database repsentation as a python object
class Database:
    def __init__(self):
        self.tables = list()

    def add_table(self, table: DatabaseTable):
        self.tables.append(table)

    def remove_table(self, table_name:str) -> int:
        for index, table in enumerate(self.tables):
            if table.name == table_name:
                self.tables.pop(index)
                return index
        return -1

    # mostly just for debugging
    # e.g. I wanted to call db(0) instead of 'db.tables[index].print_details()'
    # in order to view the contents of the table stored at index 0 in the table list
    def __call__(self, index):
        if 0 <= index < len(self.tables):
            self.tables[index].print_details()
        else:
            print("Invalid table index.")

