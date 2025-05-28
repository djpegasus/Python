from flask import Flask, render_template, request
import requests

#api bilgileri
api_key = "c172e55f02ab5e3b4ab3d9703ec9e88c"
url = "http://data.fixer.io/api/latest?access_key=" + api_key

app = Flask(__name__)

#html template bilgileri (Not: Burada free API olduğundan sadece ilk değer EUR baz almaktadır. burada çeviri kısmında para biriminleri değerleri bulunup miktarla çarpılır)
@app.route("/", methods = ["GET", "POST"]) # get ve post tanımlama
def index():
    if request.method == "POST": #eğer request method post ise
        firstCurrency = request.form.get("firstCurrency") # form içerisindeki name alanı ilk para birimi
        secondCurrency = request.form.get("secondCurrency") # form içerisindeki name alanı ikinci para birimi
        amount = request.form.get("amount") # form içerisindeki name alanı miktar birimi
        response = requests.get(url) # cevap için url gönder
        app.logger.info(response) # gönderilen url terminal bölümünde 200 değeri alıp almadığına bakılır
        infos = response.json() #json verisine çevirme
        app.logger.info(infos)# gönderilen infos terminal bölümünde json verisi olarak gelmesi
        # Çeviri
        firstValues = infos["rates"][firstCurrency] # seçilen ilk değer json verisinden seçiliyor
        secondValues = infos["rates"][secondCurrency] # seçilen ikinci değer json verisinden seçiliyor
        result = (secondValues / firstValues) * float(amount) 
        currencyInfo = dict() # sözlük oluşturulması ve bilgilerin sözlüğe eklenmesi
        currencyInfo["firstCurrency"] = firstCurrency
        currencyInfo["secondCurrency"] = secondCurrency
        currencyInfo["amount"] = amount
        currencyInfo["result"] = result
        app.logger.info(infos)
        return render_template("index.html", info = currencyInfo)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)