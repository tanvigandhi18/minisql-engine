# mini_sql_engine/web_app.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from parser.sql_parser import parse_sql
from storage.database import Database

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI()
db = Database()

class SQLQuery(BaseModel):
    query: str

# mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

@app.post("/query")
def run_query(input: SQLQuery):
    try:
        query = input.query.strip()
        if not query:
            return {"error": "Empty query"}

        if query.lower() == "show tables":
            return {"tables": list(db.tables.keys())}

        if query.lower().startswith("describe "):
            table_name = query.split()[1]
            if table_name not in db.tables:
                return {"error": f"Table '{table_name}' does not exist."}
            columns = [f"{name} ({typ})" for name, typ in db.tables[table_name].columns]
            return {"columns": columns}

        ast = parse_sql(query)
        result = db.execute(ast)
        # return {"result": result} if result else {"message": "Query executed successfully"}
        if ast["type"] == "SELECT":
            return {"result": result}
        return {"message": "Query executed successfully"}
    
    except Exception as e:
        return {"error": str(e)}
