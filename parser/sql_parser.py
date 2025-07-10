# mini_sql_engine/parser/sql_parser.py

from lark import Lark, Transformer
#select_stmt: "SELECT" "*" "FROM" NAME

sql_grammar = """
    ?start: create_stmt | insert_stmt | select_stmt | delete_stmt | update_stmt
 
    select_stmt: "SELECT" column_list "FROM" NAME where_clause?
    where_clause: "WHERE" condition
    condition: NAME "=" value
    column_list: "*"               -> select_all
            | NAME ("," NAME)*  -> select_columns


    delete_stmt: "DELETE" "FROM" NAME where_clause


    update_stmt: "UPDATE" NAME "SET" assignment where_clause
    assignment: NAME "=" value


    create_stmt: "CREATE" "TABLE" NAME "(" column_def ("," column_def)* ")"
    column_def: NAME type
    type: "INT" | "TEXT"

    insert_stmt: "INSERT" "INTO" NAME "VALUES" "(" value ("," value)* ")"
    value: SIGNED_NUMBER -> number
         | ESCAPED_STRING -> string

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    %import common.SIGNED_NUMBER
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""

parser = Lark(sql_grammar, parser='lalr')

class SQLTransformer(Transformer):
    def create_stmt(self, items):
        table_name = items[0]
        columns = [(col[0], col[1]) for col in items[1:]]
        return {"type": "CREATE", "table": str(table_name), "columns": columns}

    def insert_stmt(self, items):
        table_name = items[0]
        values = items[1:]
        return {"type": "INSERT", "table": str(table_name), "values": values}
    
    # def select_stmt(self, items):
    #     return {"type": "SELECT", "table": str(items[0])}
    
    # def select_stmt(self, items):
    #     columns = items[0]
    #     table_name = str(items[1])
    #     return {"type": "SELECT", "table": table_name, "columns": columns}
    
    def select_stmt(self, items):
        columns = items[0]
        table_name = str(items[1])
        where = items[2] if len(items) > 2 else None
        return {"type": "SELECT", "table": table_name, "columns": columns, "where": where}

    def where_clause(self, items):
        return items[0]

    def condition(self, items):
        col = str(items[0])
        val = items[1]
        return (col, val)

    def select_all(self, _):
        return ["*"]

    def select_columns(self, items):
        return [str(col) for col in items]
    
    def delete_stmt(self, items):
        table_name = str(items[0])
        where = items[1]
        return {"type": "DELETE", "table": table_name, "where": where}
    
    def update_stmt(self, items):
        table_name = str(items[0])
        assignment = items[1]
        where = items[2]
        return {"type": "UPDATE", "table": table_name, "set": assignment, "where": where}

    def assignment(self, items):
        return (str(items[0]), items[1])  # (column, new_value)

    def column_def(self, items):
        return (str(items[0]), str(items[1]))
    
    def type(self, t):
        return str(t)

    def NAME(self, token):
        return str(token)

    def number(self, token):
        return int(token[0])

    def string(self, token):
        return str(token[0][1:-1])  # remove quotes

def parse_sql(sql_text):
    tree = parser.parse(sql_text)
    return SQLTransformer().transform(tree)
