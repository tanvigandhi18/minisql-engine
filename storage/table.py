# mini_sql_engine/storage/table.py
import os
import json


class Table:
    def __init__(self, columns):
        """
        columns: list of (column_name, type) tuples
        """
        self.columns = columns
        self.rows = []

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError("Column count does not match value count.")
        
        # Simple type enforcement
        typed_values = []
        for (col_name, col_type), val in zip(self.columns, values):
            if col_type == "INT":
                if not isinstance(val, int):
                    raise ValueError(f"Expected INT for column '{col_name}' but got {type(val).__name__}")
            elif col_type == "TEXT":
                if not isinstance(val, str):
                    raise ValueError(f"Expected TEXT for column '{col_name}' but got {type(val).__name__}")
            typed_values.append(val)
        
        self.rows.append(typed_values)


    def __repr__(self):
        col_names = [col[0] for col in self.columns]
        lines = [", ".join(col_names)]
        for row in self.rows:
            lines.append(", ".join(str(val) for val in row))
        return "\n".join(lines)
    
    def select_all(self):
        return [row for row in self.rows]
    
    # def select(self, columns):
    #     if columns == ["*"]:
    #         return self.rows

    #     col_indices = [i for i, (name, _) in enumerate(self.columns) if name in columns]
    #     if len(col_indices) != len(columns):
    #         raise Exception("One or more selected columns do not exist.")
        
    #     return [[row[i] for i in col_indices] for row in self.rows]
    
    def select(self, columns, where=None):
        if columns == ["*"]:
            col_indices = list(range(len(self.columns)))
        else:
            col_indices = [i for i, (name, _) in enumerate(self.columns) if name in columns]
            if len(col_indices) != len(columns):
                raise Exception("One or more selected columns do not exist.")

        # Apply WHERE condition
        if where:
            where_col, where_val = where
            where_index = next((i for i, (name, _) in enumerate(self.columns) if name == where_col), None)
            if where_index is None:
                raise Exception(f"WHERE column '{where_col}' does not exist.")
            filtered_rows = [row for row in self.rows if row[where_index] == where_val]
        else:
            filtered_rows = self.rows

        return [[row[i] for i in col_indices] for row in filtered_rows]
    
    def delete(self, where):
        if not where:
            raise Exception("DELETE requires a WHERE clause.")

        col, val = where
        col_index = next((i for i, (name, _) in enumerate(self.columns) if name == col), None)
        if col_index is None:
            raise Exception(f"Column '{col}' not found in table.")

        original_len = len(self.rows)
        self.rows = [row for row in self.rows if row[col_index] != val]
        return original_len - len(self.rows)
    
    def update(self, assignment, where):
        set_col, set_val = assignment
        where_col, where_val = where

        set_idx = next((i for i, (name, _) in enumerate(self.columns) if name == set_col), None)
        where_idx = next((i for i, (name, _) in enumerate(self.columns) if name == where_col), None)

        if set_idx is None or where_idx is None:
            raise Exception("Invalid column in UPDATE")

        count = 0
        for row in self.rows:
            if row[where_idx] == where_val:
                row[set_idx] = set_val
                count += 1

        return count

    
    def save_to_file(self, table_name):
        os.makedirs("data", exist_ok=True)
        filepath = f"data/{table_name}.json"
        with open(filepath, "w") as f:
            json.dump({
                "columns": self.columns,
                "rows": self.rows
            }, f)

    @staticmethod
    def load_from_file(table_name):
        filepath = f"data/{table_name}.json"
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            data = json.load(f)
            t = Table(data["columns"])
            t.rows = data["rows"]
            return t



    
    

