import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-in-production")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppassword"),
    "database": os.getenv("DB_NAME", "employees"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                department VARCHAR(100) NOT NULL,
                salary DECIMAL(10,2) NOT NULL
            )
        """)
        conn.commit()
    except Error as e:
        print("Database initialization error:", e)
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

@app.route("/")
def index():
    employees = []
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees ORDER BY id DESC")
        employees = cursor.fetchall()
    except Error as e:
        flash(f"Database error: {e}", "error")
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
    return render_template("index.html", employees=employees)

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        department = request.form["department"].strip()
        salary = request.form["salary"]

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO employees (name, email, department, salary) VALUES (%s, %s, %s, %s)",
                (name, email, department, salary)
            )
            conn.commit()
            flash("Employee added successfully.", "success")
            return redirect(url_for("index"))
        except Error as e:
            flash(f"Could not add employee: {e}", "error")
        finally:
            if cursor: cursor.close()
            if conn and conn.is_connected(): conn.close()

    return render_template("add.html")

@app.route("/edit/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == "POST":
            name = request.form["name"].strip()
            email = request.form["email"].strip()
            department = request.form["department"].strip()
            salary = request.form["salary"]

            cursor.execute(
                """UPDATE employees
                   SET name=%s, email=%s, department=%s, salary=%s
                   WHERE id=%s""",
                (name, email, department, salary, employee_id)
            )
            conn.commit()
            flash("Employee updated successfully.", "success")
            return redirect(url_for("index"))

        cursor.execute("SELECT * FROM employees WHERE id=%s", (employee_id,))
        employee = cursor.fetchone()
        if not employee:
            flash("Employee not found.", "error")
            return redirect(url_for("index"))
        return render_template("edit.html", employee=employee)
    except Error as e:
        flash(f"Database error: {e}", "error")
        return redirect(url_for("index"))
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()

@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=%s", (employee_id,))
        conn.commit()
        flash("Employee deleted successfully.", "success")
    except Error as e:
        flash(f"Could not delete employee: {e}", "error")
    finally:
        if cursor: cursor.close()
        if conn and conn.is_connected(): conn.close()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    try:
        conn = get_connection()
        if conn.is_connected():
            conn.close()
            return {"status": "healthy", "database": "connected"}, 200
    except Error:
        pass
    return {"status": "unhealthy", "database": "unavailable"}, 503

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
