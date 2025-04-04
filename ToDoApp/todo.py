from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Mehmet Fazıl YAĞMUR/VS Python/ToDoApp/todo.db"
app.secret_key = '828621'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complate = db.Column(db.Boolean)
    
@app.route("/", methods=["GET", "POST"])
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

@app.route("/complate/<int:id>")
def complate(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complate = not todo.complate
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title, complate = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)