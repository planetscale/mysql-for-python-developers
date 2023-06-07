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
    room_types = []
    return dict(room_types=room_types)

@main.get("/")
def index():
    bookings = []
    return render_template("list.html", bookings=bookings)

@main.post("/create")
def create_post():
    reference_number = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10)
    )
    return redirect(url_for("main.index"))

@main.get("/create")
def create_get():
    booking = {}
    return render_template("single.html", booking=booking)

@main.get("/single/<reference_number>")
def update_get(reference_number):
    booking = {}
    if not booking:
        abort(404)

    return render_template("single.html", booking=booking)

@main.post("/single/<reference_number>")
def update_post(reference_number):
    booking = None
    if not booking:
        abort(404)
    
    return redirect(url_for("main.update_get", reference_number=reference_number))

@main.get("/delete/<reference_number>")
def delete(reference_number):
    booking = None
    if not booking:
        abort(404)
        
    return redirect(url_for("main.index"))