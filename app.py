import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
DB = "todos.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )"""
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/todos", methods=["GET"])
def list_todos():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM todos ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/todos", methods=["POST"])
def create_todo():
    text = (request.json or {}).get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    with get_db() as conn:
        cur = conn.execute("INSERT INTO todos (text) VALUES (?)", (text,))
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201


@app.route("/todos/<int:todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    with get_db() as conn:
        conn.execute("UPDATE todos SET done = NOT done WHERE id = ?", (todo_id,))
        conn.commit()
        row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    with get_db() as conn:
        conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
