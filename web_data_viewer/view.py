from flask import render_template, Blueprint, request

views = Blueprint("views", __name__)

@views.route("/")
def index():
    return render_template("index.html")
