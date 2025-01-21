from datetime import datetime
class DatabaseTable:
    def __init__(self):
        self.name = ""
        self.schema = list()
        self.data = list()

    def add_column(self, name:str, data_type:str) -> None:
        new_column = dict()
        new_column["name"] = name
        new_column["dataType"] = data_type
        self.schema.append(new_column)

    def add_rows(self, row_data:list[list]) -> None:
        self.data.extend(row_data)

    def set_name(self, name:str) -> None:
        self.name = name

    def get_column(self, column_name:str) -> tuple:
        for index, column in enumerate(self.schema):
            if column['name'] == column_name:
                column_data = [row[index] for row in self.data]
                return index, column_data
        return -1, None

    def get_column_names(self) -> list[str]:
        return [column['name'] for column in self.schema]

    def does_type_exist(self, data_type:str) -> bool:
        for column in self.schema:
            if column["dataType"] == data_type:
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
        for index, table in self.tables:
            if table["name"] == table_name:
                self.tables.pop(table)
                return index
        return -1