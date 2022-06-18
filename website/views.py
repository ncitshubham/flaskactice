from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import User, Note, Todo
from . import db
from joblib import load

views = Blueprint("views", __name__)

# Notes
@views.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    if request.method == "POST":
        new_note = request.form["note"]
        if len(new_note) > 1:
            new_note = Note(content=new_note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
    _notes = current_user.notes
    return render_template("notes.html", user=current_user, notes=_notes)


@views.route(f"/delete-note/<int:id>")
@login_required
def delete_note(id):
    note_to_delete = Note.query.get(id)

    db.session.delete(note_to_delete)
    db.session.commit()

    return redirect(url_for("views.notes"))


# Todo
@views.route("/todo", methods=["POST", "GET"])
@login_required
def todo():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        db.session.add(new_task)
        db.session.commit()

    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("todo.html", tasks=tasks, user=current_user)


@views.route(f"/delete-task/<int:id>")
@login_required
def delete_todo(id):
    task_to_del = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect(url_for("views.todo"))
    except:
        return "Issue in deleting task!"


@views.route("/update-task/<int:id>", methods=["POST", "GET"])
@login_required
def update_todo(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form["update"]

        try:
            db.session.commit()
            return redirect(url_for("views.todo"))
        except:
            return "Issue in updating task!"

    else:
        return render_template("update_todo.html", task=task_to_update, user=current_user)


# Classifier
model = load("website/spam_classifier.joblib")
messages = {"spam": "The text entered is Spam!",
           "ham": "The text entered is not spam."}


@views.route("/classify", methods=["GET", "POST"])
@login_required
def classify():
    message = ""
    text = ""
    if request.method == "POST":
        text = request.form["text"]
        prediction = model.predict([text])[0]
        message = messages.get(prediction)
    return render_template("classifier.html", text=text, message=message, user=current_user)