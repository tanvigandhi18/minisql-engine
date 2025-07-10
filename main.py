# mini_sql_engine/main.py

from parser.sql_parser import parse_sql
from storage.database import Database

db = Database()

def main():
    print("Welcome to miniSQL! Type 'exit' to quit.")
    while True:
        try:
            query = input("miniSQL > ").strip()
            if query.lower() in ("exit", "quit"):
                break
            if not query:
                continue

            # Handle internal meta-commands
            if query.lower() == "show tables":
                for name in db.tables:
                    print(name)
                continue
            if query.lower().startswith("describe "):
                table_name = query.split()[1]
                if table_name in db.tables:
                    for name, typ in db.tables[table_name].columns:
                        print(f"{name} ({typ})")
                else:
                    print(f"Table '{table_name}' does not exist.")
                continue

            ast = parse_sql(query)
            result = db.execute(ast)
            if result is not None:
                for row in result:
                    print(row)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
