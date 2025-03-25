from flask import Flask, render_template, redirect, url_for, logging, request, session, flash
from wtforms import Form, StringField, PasswordField, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__, template_folder = "mfy-content")
app.secret_key = "mfyagmur"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "personeldb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

class RegisterForm(Form):
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=4, max=30)])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyiniz."),
        validators.EqualTo("confirm", message="Parolanız Uyuşmuyor.")])
    confirm = PasswordField("Parola Doğrula")
    name = StringField("İsim", validators=[validators.Length(min=4, max=25)])
    surname = StringField("Soyisim", validators=[validators.Length(min=4, max=25)])
    dept = StringField("Departman", validators=[validators.Length(min=1, max=25)])
    unvan = StringField("Ünvan", validators=[validators.Length(min=1, max=25)])
    email = StringField("E-Posta", validators=[validators.email(message="Geçerli bir e-posta adresi giriniz.")])
    phone = StringField("Telefon", validators=[validators.Length(min=4, max=11)])

class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")
    
class UpdateForm(Form):
    name = StringField("İsim", validators=[validators.Length(min=4, max=25)])
    surname = StringField("Soyisim", validators=[validators.Length(min=4, max=25)])
    dept = StringField("Departman", validators=[validators.Length(min=1, max=25)])
    unvan = StringField("Ünvan", validators=[validators.Length(min=1, max=25)])
    email = StringField("E-Posta", validators=[validators.email(message="Geçerli bir e-posta adresi giriniz.")])
    phone = StringField("Telefon", validators=[validators.Length(min=4, max=11)])

class UpdatePassForm(Form):
    password = PasswordField("Eski Parola")
    new_pass = PasswordField("Yeni Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyiniz."),
        validators.EqualTo("confirm", message="Parolanız Uyuşmuyor.")])
    confirm = PasswordField("Parola Doğrula")

class PerRegister(Form):
    name = StringField("İsim", validators=[validators.Length(min=4, max=25)])
    surname = StringField("Soyisim", validators=[validators.Length(min=4, max=25)])
    dept = StringField("Departman", validators=[validators.Length(min=1, max=25)])
    unvan = StringField("Ünvan", validators=[validators.Length(min=1, max=25)])
    email = StringField("E-Posta", validators=[validators.email(message="Geçerli bir e-posta adresi giriniz.")])
    phone = StringField("Telefon", validators=[validators.Length(min=4, max=11)])
    age = StringField("Yaş", validators=[validators.Length(min=1, max=3)])
    salary = StringField("Maaş", validators=[validators.Length(min=1, max=10)])

  
    
@app.route("/registerPage", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password =sha256_crypt.encrypt(form.password.data)
        name = form.name.data
        surname = form.surname.data
        dept = form.dept.data
        unvan = form.unvan.data
        email = form.email.data
        phone = form.phone.data
        cursor = mysql.connection.cursor()
        query = "insert into users(username, password, name, surname, dept, unvan, email, phone) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query,(username, password, name, surname, dept, unvan, email, phone))
        mysql.connection.commit()
        cursor.close()
        flash("Kayıt Başarı ile Tamamlandı", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/loginPage", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        pass_entered = form.password.data
        cursor = mysql.connection.cursor()
        query = "select * from users where username = %s"
        result = cursor.execute(query, (username,))
        if result > 0:
            data = cursor.fetchone()
            real_pass = data["password"]
            if sha256_crypt.verify(pass_entered,real_pass):
                session["logged_in"] = True
                session["username"]= username
                session["name"] = data["name"]
                session["surname"] = data["surname"]
                session["dept"] = data["dept"]
                session["unvan"] = data["unvan"]
                session["email"] = data["email"]
                session["phone"] = data["phone"]
                session["id"] = data["id"]                
                flash("Başarı ile Giriş Yaptınız", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Parola Hatalıdır", "danger") 
                return redirect(url_for("login"))
        else:
            flash("Girdiğiniz Kullanıcı Bulunamadı.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash("Güvenli Çıkış Yapıldı.", "success")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    cursor = mysql.connection.cursor()
    query = "select * from personel"
    result = cursor.execute(query)
    if result > 0:
        personel = cursor.fetchall()
        return render_template("dashboard.html", personel = personel)
    else:
        return render_template("dashboard.html")

@app.route("/takvim")
def takvim():
    return render_template("takvim.html")

@app.route("/account")
def account():
    cursor = mysql.connection.cursor()
    query = "select * from users where username = %s"
    result = cursor.execute(query, (session["username"],))
    if result > 0:
        account = cursor.fetchone()
        return render_template("account.html", account = account)
    else:
        return render_template("account.html")

@app.route("/update", methods = ["GET", "POST"])
def update():
    form = UpdateForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        dept = form.dept.data
        newUnvan = form.unvan.data
        email = form.email.data
        phone = form.phone.data
        cursor = mysql.connection.cursor()
        query = "update users set name = %s, surname = %s, dept = %s, unvan = %s, email = %s, phone = %s where username = %s"
        cursor.execute(query,(name, surname, dept, newUnvan, email, phone, session["username"]))
        mysql.connection.commit()
        cursor.close()
        flash("Bilgileriniz Güncellendi", "success")
        return redirect(url_for("account"))
    return render_template("update.html", form=form)

@app.route("/updatePass", methods = ["GET", "POST"])
def updatePass():
    form = UpdatePassForm(request.form)
    if request.method == "POST" and form.validate():
        password = form.password.data
        new_pass = sha256_crypt.encrypt(form.new_pass.data)
        cursor = mysql.connection.cursor()
        query = "select * from users where username = %s"
        result = cursor.execute(query, (session["username"],))
        if result > 0:
            data = cursor.fetchone()
            real_pass = data["password"]
            if sha256_crypt.verify(password,real_pass):
                query = "update users set password = %s where username = %s"
                cursor.execute(query,(new_pass, session["username"]))
                mysql.connection.commit()
                cursor.close()
                flash("Parolanız Güncellendi", "success")
                return redirect(url_for("account"))
            else:
                flash("Eski Parolanız Hatalıdır", "danger")
                return redirect(url_for("updatePass"))
    return render_template("updatePass.html", form=form)

@app.route("/perRegister", methods = ["GET", "POST"])
def perRegister():
    form = PerRegister(request.form)
    if request.method == "POST":
        name = form.name.data
        surname = form.surname.data
        dept = form.dept.data
        unvan = form.unvan.data
        email = form.email.data
        phone = form.phone.data
        age = form.age.data
        salary = form.salary.data
        cursor = mysql.connection.cursor()
        query = "insert into personel(name, surname, dept, unvan, email, phone, age, salary) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (name, surname, dept, unvan, email, phone, age, salary))
        mysql.connection.commit()
        cursor.close()
        flash("Personel Başarı ile Eklendi", "success")
        return redirect(url_for("dashboard"))
    return render_template("perRegister.html", form=form)

@app.route("/perList")
def perList():
    cursor = mysql.connection.cursor()
    query = "select * from personel"
    result = cursor.execute(query)
    if result > 0:
        personel = cursor.fetchall()
        return render_template("perList.html", personel = personel)
    else:
        return render_template("perList.html")

@app.route("/readPage/<string:id>")
def readPage(id):
    pass

@app.route("/updatePage/<string:id>")
def updatePage(id):
    pass

@app.route("/delete/<string:id>")
def delete(id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
    
