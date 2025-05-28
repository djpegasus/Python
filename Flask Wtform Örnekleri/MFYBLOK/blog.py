from flask import Flask, render_template,flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

# User Registration Form Class
class RegisterForm(Form):
    name = StringField("Adı Soyadı", validators=[validators.Length(min=4, max=25, message="Lütfen geçerli bir isim girin.")])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5, max=35, message="Lütfen geçerli bir kullanıcı adı girin.")])
    email = StringField("Email Adresi", validators=[validators.email(message="Lütfen geçerli bir email adresi girin.")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyin."),
        validators.EqualTo(fieldname="confirm", message="Parolanız uyuşmuyor.")
    ])
    confirm = PasswordField("Parola Doğrula")

class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

app = Flask(__name__, template_folder="template") #template_folder="template" is used to change the default template folder to the new folder named template
app.secret_key = "mfyblog"  #secret_key is used to create a session for the user
app.config['MYSQL_HOST'] = "localhost"  #localhost is the default host
app.config['MYSQL_USER'] = "root"     #root is the default user
app.config['MYSQL_PASSWORD'] = ""   #password is the default password
app.config['MYSQL_DB'] = "mfyblog"  #mfyblog is the default database


# Extra configs, optional:
app.config['MYSQL_CURSORCLASS'] = "DictCursor"  #DictCursor is used to return the data in the form of dictionary
mysql = MySQL(app)

# Home page
@app.route('/') 
def index():
    return render_template('index.html')

# Login control decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen giriş yapın...", "danger")
            return redirect(url_for("login"))
    return decorated_function

# Register page
@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name=form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
# Create a cursor
        cursor = mysql.connection.cursor()
# Query to insert the data into the database
        sorgu = "Insert into users(name, email, username, password) VALUES(%s, %s, %s, %s)"
        cursor.execute(sorgu, (name, email, username, password))
# Commit to database
        mysql.connection.commit()
# Close the connection
        cursor.close()
        flash("Başarıyla kayıt oldunuz...", "success")
        return redirect(url_for("login"))
    else:
        return render_template('register.html', form = form)

# Login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "Select * from users where username = %s"
        result = cursor.execute(sorgu, (username,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data['password']
            if sha256_crypt.verify(password_entered, real_password):
                flash("Başarıyla giriş yaptınız...", "success")

                session["logged_in"] = True
                session["username"] = username

                return redirect(url_for("index"))
            else:
                flash("Parolanızı yanlış girdiniz...", "danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor...", "danger")
            return redirect(url_for("login"))

    return render_template('login.html', form = form)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    cursor = mysql.connection.cursor()
    sorgu = 'Select * From articles'
    result = cursor.execute(sorgu)
    if result > 0:
        articles = cursor.fetchall()
        return render_template('articles.html', articles=articles)
    else:
        return render_template('articles.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = 'Select * From articles where author = %s'
    result = cursor.execute(sorgu,(session['username'],))
    if result > 0:
        articles = cursor.fetchall()
        return render_template('dashboard.html', articles=articles)
    else:
        return render_template('dashboard.html')

@app.route('/addarticle', methods=['GET', 'POST'])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()
        sorgu = 'Insert into articles(title,author,content) VALUE (%s,%s,%s)'
        cursor.execute(sorgu,(title,session['username'],content))
        mysql.connection.commit()
        cursor.close()
        flash("Makale Başarıyla Eklenmiştir.", "success")
        return redirect(url_for("dashboard"))
    return render_template('addarticle.html', form=form)

class ArticleForm(Form):
    title = StringField('Makale Başlığı', validators=[validators.Length(min=5, max=100)])
    content = TextAreaField('Makale İçeriği', validators=[validators.Length(min=10)])

# Detay Sayfası
@app.route('/article/<string:id>')
def article(id):
    cursor = mysql.connection.cursor()
    sorgu = 'select * from articles where id = %s'
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template('article.html', article=article)
    else:
        return render_template('article.html')

#Makale Silme
@app.route('/delete/<string:id>')
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles where author = %s and id = %s"
    result = cursor.execute(sorgu,(session['username'],id))

    if result > 0:
        sorgu2 = "delete from articles where id= %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for('dashboard'))
    else:
        flash("Böyle Bir Makale Yok veya İşlemYetkiniz Yok...","danger")
        return redirect(url_for('index'))
    
#Makale Güncelleme
@app.route("/edit/<string:id>", methods =["GET","POST"])
@login_required
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "select * from articles where id=%s and author  = %s"
        result = cursor.execute(sorgu,(id,session["username"]))
        if result == 0:
            flash("Böyle Bir Makale Bulunamamıştır.", "danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html", form=form)
    else:
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data
        sorgu2 = "Update articles Set title = %s,content=%s where id=%s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newTitle,newContent,id))
        mysql.connection.commit()
        flash("İşlem Başarıyla Gerçekleşmiştir.", "success")
        return redirect(url_for("dashboard"))

@app.route("/search", methods =["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "select * from articles where title like '%" + keyword + "%' "
        result = cursor.execute(sorgu)
        
        if result == 0:
            flash("Araığınız Kelime Bulunamadı", "warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)