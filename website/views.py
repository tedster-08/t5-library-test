from flask import render_template, Blueprint, request, jsonify
import json
from .models import MeritBadgePamphlet
from . import db

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/library")
def library():
    books = MeritBadgePamphlet.query.order_by(
        MeritBadgePamphlet.title).all()
    print(books)
    return render_template("library.html", books=books)


@views.route("/add-book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":

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
            "Family Life"
        ]

        title = request.form.get("title")
        is_up_to_date = (request.form.get("indate") == "on")
        is_eagle_required = (title in eagle_required_badges)

        new_pamphlet = MeritBadgePamphlet(
            title=title, is_up_to_date=is_up_to_date, is_eagle_required=is_eagle_required, is_checked_out=False)
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


# @views.route("/librarian")
# def librarian():
#     books = MeritBadgePamphlet.query.filter_by(is_checked_out=True).all()
#     print(books)
#     return render_template("librarian.html", checked_out_books=books)


def _shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@views.route("/shut")
def shutdown_server_from_url():
    print("Shutdown URL accessed, shutting down!")
    _shutdown_server()
    return "Server shutting down!"
