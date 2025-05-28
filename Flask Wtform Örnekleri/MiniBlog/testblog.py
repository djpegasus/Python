from flask import Flask,render_template,session,url_for,logging,flash,redirect,request
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form,StringField,PasswordField,TextAreaField,validators
from functools import wraps

class RegisterForm(Form):
    name = StringField("Adı Soyadı", validators=[validators.Length(min=4, max=25)])
    email = StringField("E-Posta", validators=[validators.email(message="Mail Formatı Olmalıdır...")])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=4, max=25)])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Bir Parola Belirleyiniz."),
        validators.EqualTo("confirm", message="Parola Uyuşmamaktadır.")
    ])
    confirm = PasswordField("Parola Doğrula")

class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

class ArticleForm(Form):
    title = StringField("Başlık", validators=[validators.Length(min=4)])
    content = StringField("İçerik Yazısı", validators=[validators.Length(min=10)])
    
app = Flask(__name__, template_folder="template")
app.secret_key="testblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "testdb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("logged_in"):
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın...", "danger")
            return redirect("login")
    return decorated_func

@app.route("/register", methods = ["GET", "POST"])
def reegister():
    form = RegisterForm(request.form)
    if request.method=="POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)
        cursor =mysql.connection.cursor()
        query = "Insert into users(name,email,username,password) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash("Başarıyla Kayıt Oldunuz...", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        pass_enter = form.password.data
        cursor = mysql.connection.cursor()
        query = "Select * from users where username = %s"
        result = cursor.execute(query,(username,))
        if result > 0:
            data = cursor.fetchone()
            pass_real = data["password"]
            if sha256_crypt.verify(pass_enter,pass_real):
                session["logged_in"] = True
                session["username"] = username
                flash("Giriş Yapıldı.", "success")
                return redirect(url_for("index"))
            else:
                flash("Parolanız Hatalıdır.", "warning")
                return redirect(url_for("login"))
        else:
            flash("Böyle Bir Kullanıcı Bulunmamaktadır", "danger")
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

@app.route("/panel")
@logged_in
def panel():
    cursor = mysql.connection.cursor()
    query = "select * from forum where author = %s"
    result = cursor.execute(query,(session["username"],))
    if result > 0:
        data = cursor.fetchall()
        return render_template("panel.html", data=data)
    else:
        return render_template("panel.html")

@app.route("/forum")
def forum():
    cursor = mysql.connection.cursor()
    query = "select * from forum"
    result = cursor.execute(query)
    if result > 0:
        liste = cursor.fetchall()
        return render_template("forum.html", liste=liste)
    else:
        return render_template("forum.html")

@app.route("/news")
def news():
    return render_template("haberler.html")

@app.route("/video")
def video():
    return render_template("video.html")

@app.route("/addarticle", methods = ["GET", "POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST":
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()
        query = "Insert into forum (title,author,content) VALUE (%s,%s,%s)"
        cursor.execute(query,(title,session["username"],content))
        mysql.connection.commit()
        cursor.close()
        flash("İçerik Kaydedilmiştir...","success")
        return redirect(url_for("panel"))
    return render_template("addarticle.html", form=form)

@app.route("/contents/<string:id>")
def contents(id):
    cursor = mysql.connection.cursor()
    query = "select * from forum where id = %s"
    result = cursor.execute(query,(id,))
    if result > 0:
        content = cursor.fetchone()
        return render_template("contents.html", content=content)
    else:
        return render_template("contents.html")
    
@app.route("/update/<string:id>", methods = ["GET", "POST"])
@logged_in
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        query = "select * from forum where id=%s and author =%s"
        result = cursor.execute(query,(id,session["username"]))
        if result == 0 :
            flash("Böylke Bir Makele Bulunamamıştır.", "danger")
            return redirect(url_for("panel"))
        else:
            content = cursor.fetchone()
            form = ArticleForm()
            form.title.data = content["title"]
            form.content.data = content["content"]
            return render_template("update.html", form=form)
    else:
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data
        query2 ="update forum set title = %s and content= %s where id =%s"
        cursor = mysql.connection.cursor()
        cursor.execute(query2,(newTitle,newContent,id))
        mysql.connection.commit()
        flash("Değişiklikler Kaydedilmiştir.", "success")
        return redirect(url_for("panel"))
    
@app.route("/delete/<string:id>")
@logged_in
def delete(id):
    cursor = mysql.connection.cursor()
    query = "select * from forum where id=%s and author =%s"
    result = cursor.execute(query,(id,session["username"]))
    if result > 0:
        query2 = "delete from forum where id = %s"    
        cursor.execute(query2,(id,))
        mysql.connection.commit()
        return redirect(url_for("panel"))
    else:
        flash("Böyle Bir Makale Yok veya İşlemYetkiniz Yok...","danger")
        return redirect(url_for('panel'))

@app.route("/search", methods =["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "select * from forum where title like '%" + keyword + "%' "
        result = cursor.execute(sorgu)
        if result > 0:
            liste = cursor.fetchall()
            return render_template("forum.html", liste=liste)
        else:
            flash("Araığınız Kelime Bulunamadı", "warning")
            return redirect(url_for("forum"))

if __name__ == "__main__":
    app.run(debug=True)