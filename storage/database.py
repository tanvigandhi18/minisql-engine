# mini_sql_engine/storage/database.py

from storage.table import Table
import os


class Database:
    def __init__(self):
        self.tables = {}
        self.load_tables()

    def load_tables(self):
        if not os.path.exists("data"):
            return
        for file in os.listdir("data"):
            if file.endswith(".json"):
                table_name = file.replace(".json", "")
                table = Table.load_from_file(table_name)
                if table:
                    self.tables[table_name] = table

    def execute(self, ast):
        if ast["type"] == "CREATE":
            self.create_table(ast)
        elif ast["type"] == "INSERT":
            self.insert_into_table(ast)
        elif ast["type"] == "SELECT":
            return self.select_from_table(ast)
        elif ast["type"] == "DELETE":
            return self.delete_from_table(ast)
        elif ast["type"] == "UPDATE":
            return self.update_table(ast)
        else:
            raise ValueError(f"Unsupported query type: {ast['type']}")

    def create_table(self, ast):
        table_name = ast["table"]
        if table_name in self.tables:
            raise Exception(f"Table '{table_name}' already exists.")
        self.tables[table_name] = Table(ast["columns"])
        print(f"Table '{table_name}' created.")
        self.tables[table_name].save_to_file(table_name)

    def insert_into_table(self, ast):
        table_name = ast["table"]
        if table_name not in self.tables:
            raise Exception(f"Table '{table_name}' does not exist.")
        self.tables[table_name].insert(ast["values"])
        print(f"1 row inserted into '{table_name}'.")
        self.tables[table_name].save_to_file(table_name)

    # def select_from_table(self, ast):
    #     table_name = ast["table"]
    #     if table_name not in self.tables:
    #         raise Exception(f"Table '{table_name}' does not exist.")
    #     return self.tables[table_name].select_all()

    # def select_from_table(self, ast):
    #     table_name = ast["table"]
    #     columns = ast["columns"]
    #     if table_name not in self.tables:
    #         raise Exception(f"Table '{table_name}' does not exist.")
    #     return self.tables[table_name].select(columns)
    
    def select_from_table(self, ast):
        table_name = ast["table"]
        columns = ast["columns"]
        where = ast.get("where")
        if table_name not in self.tables:
            raise Exception(f"Table '{table_name}' does not exist.")
        return self.tables[table_name].select(columns, where)
    
    def delete_from_table(self, ast):
        table_name = ast["table"]
        where = ast.get("where")
        if table_name not in self.tables:
            raise Exception(f"Table '{table_name}' does not exist.")
        count = self.tables[table_name].delete(where)
        print(f"{count} row(s) deleted from '{table_name}'.")
        self.tables[table_name].save_to_file(table_name)

    def update_table(self, ast):
        table_name = ast["table"]
        if table_name not in self.tables:
            raise Exception(f"Table '{table_name}' does not exist.")
        count = self.tables[table_name].update(ast["set"], ast["where"])
        self.tables[table_name].save_to_file(table_name)
        print(f"{count} row(s) updated in '{table_name}'.")



