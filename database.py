class DatabaseTable:
    def __init__(self):
        self.name = ""
        self.schema = list()
        self.data = list()

    def get_column(self, column_name:str) -> tuple:
        for index, column in enumerate(self.schema):
            if column["Field"] == column_name:
                column_data = [row[column_name] for row in self.data]
                return index, column_data
        return -1, None

    def get_column_by_index(self, index:int) -> tuple:
        found = False
        column_data = list()
        try:
            column_data.extend([row[index] for row in self.data])
            found = True
        except KeyError as e:
            print(f"Failed to get data from index = {index} : {e}")
        return found, column_data

    def get_column_type(self, column_name:str) -> tuple:
        for index, column in enumerate(self.schema):
            if column["Field"] == column_name:
                return index, column["Type"]
        return -1, None

    def does_type_exist(self, data_type:str) -> bool:
        for column in self.schema:
            if column["Type"] == data_type:
                return True
        return False

    def print_details(self) -> None:
        print(f"""
        Database Name: {self.name}
        Database Schema: {self.schema}
        Data Sample(5): {self.data[:5]}
            """)

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

    def __call__(self, index):
        if 0 <= index < len(self.tables):
            self.tables[index].print_details()
        else:
            print("Invalid table index.")

