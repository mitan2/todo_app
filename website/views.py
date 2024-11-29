from flask import Blueprint, redirect, render_template, url_for, request
from website.models import Todo
from website import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    message = request.args.get('message', None)
    return render_template("index.html", todo_list=todo_list, message=message)

@my_view.route("/add", methods=["POST"])
def add():
    try:
        task = request.form.get("task")
        new_todo = Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        message = "Task added successfully."
        return redirect(url_for("my_view.home", message=message))
    except:
        message = "There was an error adding your task. Please try again."
        return redirect(url_for("my_view.home", message=message))

@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    message = "Task marked as complete." if todo.complete else "Task marked as incomplete."
    return redirect(url_for("my_view.home", message=message))

@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    message = "Task deleted successfully."
    return redirect(url_for("my_view.home", message=message))

@my_view.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if request.method == "POST":
        new_task = request.form.get("task")
        todo.task = new_task
        db.session.commit()
        message = "Task edited successfully."
        return redirect(url_for("my_view.home", message=message))
    return render_template("edit.html", todo=todo)