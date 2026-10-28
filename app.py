
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import date

app = Flask(__name__)
app.secret_key = "appointment-system-devops"


DATABASE = os.environ.get(
    "DATABASE",
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "appointments.db"
    )
)

CATEGORIES = [
    "General Consultation",
    "Personal Meeting",
    "Technical Support"
]


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            category TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Booked',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    search = request.args.get("search", "").strip()

    connection = get_db_connection()

    if search:
        appointments = connection.execute("""
            SELECT * FROM appointments
            WHERE name LIKE ? OR CAST(id AS TEXT) = ?
            ORDER BY appointment_date, appointment_time
        """, (f"%{search}%", search)).fetchall()
    else:
        appointments = connection.execute("""
            SELECT * FROM appointments
            ORDER BY appointment_date, appointment_time
        """).fetchall()

    connection.close()

    return render_template(
        "index.html",
        appointments=appointments,
        categories=CATEGORIES,
        today=date.today().isoformat(),
        search=search
    )


@app.route("/book", methods=["POST"])
def book_appointment():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    category = request.form.get("category", "").strip()
    appointment_date = request.form.get("date", "").strip()
    appointment_time = request.form.get("time", "").strip()

    # Validate required fields
    if not all([
        name, email, phone, category,
        appointment_date, appointment_time
    ]):
        flash("Please fill in all the fields.", "error")
        return redirect(url_for("home"))

    # Validate appointment category
    if category not in CATEGORIES:
        flash("Please select a valid appointment category.", "error")
        return redirect(url_for("home"))

    # Validate date and time formats
    try:
        selected_date = date.fromisoformat(appointment_date)
        hour, minute = map(int, appointment_time.split(":"))

        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError

    except (ValueError, TypeError):
        flash("Please enter a valid appointment date and time.", "error")
        return redirect(url_for("home"))

    # Prevent past appointments
    if selected_date < date.today():
        flash("Past dates cannot be selected.", "error")
        return redirect(url_for("home"))

    # Basic email validation
    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Please enter a valid email address.", "error")
        return redirect(url_for("home"))

    # Basic phone validation
    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        flash("Enter a phone number containing 10 to 15 digits.", "error")
        return redirect(url_for("home"))

    connection = get_db_connection()

    # Prevent duplicate active time slots
    existing = connection.execute("""
        SELECT id FROM appointments
        WHERE appointment_date = ?
          AND appointment_time = ?
          AND status = 'Booked'
    """, (appointment_date, appointment_time)).fetchone()

    if existing:
        connection.close()
        flash(
            "This time slot is already booked. Please select another time.",
            "error"
        )
        return redirect(url_for("home"))

    cursor = connection.execute("""
        INSERT INTO appointments (
            name, email, phone, category,
            appointment_date, appointment_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name, email, phone, category,
        appointment_date, appointment_time
    ))

    appointment_id = cursor.lastrowid

    connection.commit()
    connection.close()

    flash(
        f"Appointment booked successfully! Your Appointment ID is {appointment_id}.",
        "success"
    )

    return redirect(url_for("home"))


@app.route("/cancel/<int:appointment_id>", methods=["POST"])
def cancel_appointment(appointment_id):
    connection = get_db_connection()

    appointment = connection.execute("""
        SELECT id, status FROM appointments
        WHERE id = ?
    """, (appointment_id,)).fetchone()

    if appointment is None:
        flash("Appointment not found.", "error")

    elif appointment["status"] == "Cancelled":
        flash("This appointment is already cancelled.", "error")

    else:
        connection.execute("""
            UPDATE appointments
            SET status = 'Cancelled'
            WHERE id = ?
        """, (appointment_id,))

        connection.commit()
        flash("Appointment cancelled successfully.", "success")

    connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=True)