from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status INTEGER DEFAULT 0
        )
    """)
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]
    priority = request.form["priority"]
    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO tasks(task, priority) VALUES(?, ?)", (task, priority))

    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/complete/<int:id>")
def complete(id):
    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE tasks SET status=1 WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        new_task = request.form["task"]
        new_priority = request.form["priority"]
        cur.execute("UPDATE tasks SET task=?, priority=? WHERE id=?", (new_task, new_priority, id))

        conn.commit()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = cur.fetchone()
    conn.close()
    return render_template("update.html", task=task)

if __name__ == "__main__":
    app.run(debug=True)
