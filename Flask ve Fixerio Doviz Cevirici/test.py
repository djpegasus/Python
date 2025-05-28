from flask import Flask, render_template, request
import requests

api_key = "c172e55f02ab5e3b4ab3d9703ec9e88c"
url = "http://data.fixer.io/api/latest?access_key=" + api_key

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        firstCurrency = request.form.get("firstCurrency")
        secondCurrency = request.form.get("secondCurrency")
        amount = request.form.get("amount")
        response = requests.get(url)
        infoJson = response.json()
        firstValue = infoJson["rates"][firstCurrency]
        secondValue = infoJson["rates"][secondCurrency]
        result = (secondValue/firstValue) * float(amount)
        infoDict = dict()
        infoDict["firstCurrency"] = firstCurrency
        infoDict["secondCurrency"] = secondCurrency
        infoDict["amount"] = amount
        infoDict["result"] = result
        return render_template ("index.html", info = infoDict)        
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)