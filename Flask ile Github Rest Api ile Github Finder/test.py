from flask import Flask, render_template, request
import requests

app = Flask(__name__)
url = "https://api.github.com/users/"

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        gitname = request.form.get("githubname")
        user_api = requests.get(url + gitname)
        repos_api = requests.get(url + gitname + "/repos")
        user_info = user_api.json()
        repos = repos_api.json()
        if "message" in user_info:
            return render_template("index.html", error = "Kullanıcı Kaydı Bulunamadı...")
        else:
            return render_template("index.html", profile = user_info, repos = repos)
    else:
        return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)