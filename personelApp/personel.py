from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="webtemplate")
app.secret_key="828621"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Users/Mehmet Fazıl YAĞMUR/VS Python/personelApp/personel.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    maas = db.Column(db.Integer, nullable=False)
    job = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Boolean, default=False)
    
class registerUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    repassword = db.Column(db.String(50), nullable=False)
    
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login = registerUser.query.filter_by(username=username, password=password).first()
        if login:
            session["username"]= username
            return redirect(url_for("dashboard"))
        else:
            return "Username or Password is in correct"
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        repassword = request.form["repassword"]
        if password == repassword:
            new_user = registerUser(username=username, password=password, repassword=repassword)
            db.session.add(new_user),
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/addPer", methods=["GET", "POST"])
def addPer():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        job = request.form["job"]
        maas = request.form["maas"]
        new_user = User(name=name, surname=surname, email=email, maas=maas, job=job, status=False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("addper.html")

@app.route("/dashboard")
def dashboard():
    users = User.query.all()
    return render_template("dashboard.html", users=users)

@app.route("/status/<int:id>")
def status(id):
    user =User.query.filter_by(id=id).first()
    user.status = not user.status
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/delete/<int:id>")
def delete(id):
    user =User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    