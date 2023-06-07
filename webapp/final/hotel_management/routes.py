import random
import string

from flask import (
    abort,
    Blueprint, 
    redirect, 
    request, 
    render_template, 
    url_for
)

from .db import get_db

main = Blueprint("main", __name__)

@main.context_processor
def get_room_types():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT code, description FROM room_type;")
    room_types = cursor.fetchall()
    cursor.close()
    return dict(room_types=room_types)

@main.get("/")
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            booking.reference_number,
            guest.name,
            booking.check_in,
            booking.check_out,
            room_type.description,
            booking.airport_pickup_time,
            booking.breakfast
        FROM booking
        JOIN guest ON booking.guest_id = guest.id
        JOIN room_type ON booking.room_type_id = room_type.id;
        """
    )

    bookings = cursor.fetchall()
    cursor.close()
    return render_template("list.html", bookings=bookings)

@main.post("/create")
def create_post():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name FROM guest WHERE email = %s;",
        [request.form["email"]]
    )

    guest = cursor.fetchone()

    if guest:
        guest_id = guest["id"]
        if request.form["name"] != guest["name"]:
            cursor.execute(
                "UPDATE guest SET name = %s WHERE id = %s;",
                [request.form["name"], guest_id]
            )
    else:
        cursor.execute(
            "INSERT INTO guest (name, email) VALUES (%s, %s);",
            [request.form["name"], request.form["email"]]
        )
        guest_id = cursor.lastrowid

    cursor.execute(
        "SELECT id FROM room_type WHERE code = %s;",
        [request.form["room_type"]]
    )

    room_type = cursor.fetchone()

    reference_number = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )

    cursor.execute(
        """
        INSERT INTO booking (
            check_in,
            check_out,
            guest_id,
            reference_number,
            breakfast,
            airport_pickup_time,
            room_type_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """,
        [
            request.form["check_in"],
            request.form["check_out"],
            guest_id,
            reference_number,
            bool(request.form.get("breakfast")),
            request.form["airport_pickup_time"],
            room_type["id"]
        ]
    )

    db.commit()

    cursor.close()
    return redirect(url_for("main.index"))

@main.get("/create")
def create_get():
    booking = {}
    return render_template("single.html", booking=booking)

@main.get("/single/<reference_number>")
def update_get(reference_number):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute(
        """
        SELECT
            booking.reference_number,
            guest.name,
            guest.email,
            booking.check_in,
            booking.check_out,
            room_type.code,
            booking.airport_pickup_time,
            booking.breakfast
        FROM booking
        JOIN guest ON booking.guest_id = guest.id
        JOIN room_type ON booking.room_type_id = room_type.id
        WHERE booking.reference_number = %s;"
        """,
        [reference_number]
    )
    
    booking = cursor.fetchone()
    
    if not booking:
        cursor.close()
        abort(404)
    
    cursor.close()
    return render_template("single.html", booking=booking)

@main.post("/single/<reference_number>")
def update_post(reference_number):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT guest_id FROM booking WHERE reference_number = %s",
        [reference_number]
    )

    booking = cursor.fetchone()

    if not booking:
        abort(404)

    cursor.execute(
        "UPDATE guest SET name = %s, email = %s WHERE id = %s",
        [request.form["name"], request.form["email"], booking["guest_id"]]
    )

    cursor.execute(
        """
        UPDATE booking
        JOIN room_type ON code = %s
        SET
            check_in = %s,
            check_out = %s,
            room_type_id = room_type.id,
            breakfast = %s,
            airport_pickup_time = %s
        WHERE reference_number = %s;
        """,
        [
            request.form["room_type"],
            request.form["check_in"],
            request.form["check_out"],
            bool(request.form.get("breakfast")),
            request.form["airport_pickup_time"],
            reference_number
        ]
    )

    db.commit()
    cursor.close()
    
    return redirect(url_for("main.update_get", reference_number=reference_number))

@main.get("/delete/<reference_number>")
def delete(reference_number):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT 1 FROM booking WHERE reference_number = %s;",
        [reference_number]
    )

    booking = cursor.fetchone()

    if not booking:
        cursor.close()
        abort(404)

    cursor.execute(
        "DELETE FROM booking WHERE reference_number = %s",
        [reference_number]
    )
    db.commit()
    cursor.close()
        
    return redirect(url_for("main.index"))