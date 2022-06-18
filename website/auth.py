from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email doesn't exist. Try again!", category="error")
        elif check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash("Login Successfully!", category="success")
            return redirect(url_for("views.notes"))
        else:
            flash("Password doesn't match! Try again.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!", category="error")
        elif len(email) < 4:
            flash("Email should be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First Name should be greater than 1 character.", category="error")
        elif password2 != password1:
            flash("Passwords don't match", category="error")
        elif len(password1) < 5:
            flash("Password should be greater than 4 characters.", category="error")
        else:
            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for("views.notes"))

    return render_template("signup.html", user=current_user)
