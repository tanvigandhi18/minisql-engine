
**MiniSQL: Custom Relational Query Engine in Python**

MiniSQL is a lightweight SQL engine developed from scratch in Python. It can parse and execute SQL queries on in-memory tables, using a custom grammar built with Lark. The project includes both a command-line interface and a FastAPI-powered web interface, featuring drag-and-drop SQL block support and live result visualization.

---

**Key Features:**

* Custom SQL grammar parser using Lark (AST-based design)
* Supports key SQL operations:

  * CREATE TABLE
  * INSERT INTO ... VALUES (...)
  * SELECT with column filtering and WHERE clauses
  * UPDATE ... SET ... WHERE
  * DELETE FROM ... WHERE
* In-memory data storage with schema validation
* Persistent table storage via auto-saved JSON files
* Web interface features:

  * Drag-and-drop SQL query builder
  * Interactive HTML-based result display
  * REST API for query execution

---
## Sample Queries

```sql
CREATE TABLE students (id INT, name TEXT);
INSERT INTO students VALUES (1, "Alice");
INSERT INTO students VALUES (2, "Bob");

SELECT * FROM students;
SELECT name FROM students WHERE id = 1;

UPDATE students SET name = "Charlie" WHERE id = 2;
DELETE FROM students WHERE name = "Charlie";
````
---

## How to Run

### CLI Mode

```bash
python main.py
```

### Web Interface

```bash
uvicorn web_app:app --reload
```

Then open: [http://localhost:8000](http://localhost:8000)
Optional Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Project Structure

```
mini_sql_engine/
├── parser/              # SQL grammar and AST transformer
│   └── sql_parser.py
├── storage/             # Table schema, data, and engine logic
│   ├── database.py
│   └── table.py
├── static/              # Web UI (HTML, CSS, JS)
│   └── index.html
├── data/                # Auto-saved JSON files per table
├── main.py              # CLI REPL for SQL input
├── web_app.py           # FastAPI web backend
├── requirements.txt     # Project dependencies
└── README.md
```

---

## Screenshots

> Visuals from the drag-and-drop web interface and query results:

![Query UI](static/Screenshot1.png)
![Query Result Table](static/Screenshot2.png)

---

## Dependencies

* Python 3.7+
* [`lark`](https://github.com/lark-parser/lark)
* [`fastapi`](https://fastapi.tiangolo.com/)
* [`uvicorn`](https://www.uvicorn.org/)

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Why This Project Matters

This project demonstrates:

* How relational databases work under the hood
* SQL grammar design and AST parsing
* State management, data persistence, and web service integration
* Full-stack integration of backend logic and frontend interaction

---

## Future Improvements

* `AND`/`OR` support in `WHERE` clauses
* Named column projections with real schema header display
* Joins between tables
* SQLite-style `.sql` file runner
* Result download as CSV
* Admin interface to browse all tables

---

## License

This project is for educational purposes and open to contributions and extension.

---

## Author

Developed as a hands-on demonstration of database systems and full-stack engineering.

