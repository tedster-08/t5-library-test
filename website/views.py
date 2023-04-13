from flask import render_template, Blueprint, request, jsonify, redirect
import json
import csv
import os
from .models import MeritBadgePamphlet
from . import db

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/library")
def library():
    books = MeritBadgePamphlet.query.order_by(MeritBadgePamphlet.title).all()
    print(books)
    return render_template("library.html", books=books)


def _is_eagle_required(book):

    eagle_required_badges = [
        "First Aid",
        "Citizenship in the Community",
        "Citizenship in the Nation",
        "Citizenship in Society",
        "Citizenship in the World",
        "Communication",
        "Cooking",
        "Personal Fitness",
        "Emergency Preparedness",
        "Lifesaving",
        "Environmental Science",
        "Sustainability",
        "Personal Management",
        "Swimming",
        "Hiking",
        "Cycling",
        "Camping",
        "Family Life",
    ]

    return book in eagle_required_badges


@views.route("/add-book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        is_up_to_date = request.form.get("indate") == "on"
        is_eagle_required = _is_eagle_required(title)

        new_pamphlet = MeritBadgePamphlet(
            title=title,
            is_up_to_date=is_up_to_date,
            is_eagle_required=is_eagle_required,
            is_checked_out=False,
        )
        db.session.add(new_pamphlet)
        db.session.commit()
    return render_template("add_book.html")


@views.route("/check-out", methods=["POST"])
def check_out():
    data = json.loads(request.data)
    book = MeritBadgePamphlet.query.get(data["id"])
    if book:
        book.is_checked_out = True
        book.checked_out_to = data["name"]
        db.session.commit()
        print(f"Checked out {book.title} to {data['name']}.")
    return jsonify({})


@views.route("/check-in", methods=["POST"])
def check_in():
    data = json.loads(request.data)
    book = MeritBadgePamphlet.query.get(data["id"])
    if book:
        book.is_checked_out = False
        book.checked_out_to = None
        db.session.commit()
        print(f"Checked in {book.title}")
    return jsonify({})


@views.route("/librarian")
def librarian():
    books = MeritBadgePamphlet.query.filter_by(is_checked_out=True).all()
    print(books)
    return render_template("librarian.html", checked_out_books=books)


def _shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@views.route("/shut")
def shutdown_server_from_url():
    print("Shutdown URL accessed, shutting down!")
    _shutdown_server()
    return "Server shutting down!"


@views.route("/libauth")
def libauth():
    return render_template("libauth.html")


@views.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)
        if file:
            file.save("temp-data.csv")
            with open("temp-data.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    next(reader)
                    title, in_date, checked_out, checked_out_to = row
                    in_date = False if in_date == 0 else True
                    checked_out = False if checked_out == 0 else True
                    new_pamphlet = MeritBadgePamphlet(
                        title=title,
                        is_up_to_date=in_date,
                        is_eagle_required=_is_eagle_required(
                            title),
                        is_checked_out=checked_out,
                        checked_out_to=checked_out_to,
                    )

                    db.session.add(new_pamphlet)
        db.session.commit()
        os.remove("temp-data.csv")

    return render_template("upload.html")
