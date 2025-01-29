import sqlite3
from PyQt6.QtWidgets import QApplication,QMainWindow
from registerUI import Ui_regForm
import sys

class RegisterWindow(QMainWindow,Ui_regForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.crmdb()

        self.reg_saveButton.clicked.connect(self.regSave)
        self.reg_clearButton.clicked.connect(self.reg_clear)

    def crmdb(self):
        self.connect = sqlite3.connect("C:/Sqlite/CrmDB.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute("create table if not exists mfy_users (username TEXT, password TEXT)")
        self.connect.commit()

    def crmdbClose(self):
        self.connect.close()

    def regSave(self):
        username = self.regLine_user.text()
        password = self.regLine_pw.text()
        repassword = self.regLine_repw.text()
        if  password != repassword:
            self.reg_label_status.setText("Şifre Birbiri ile Uyuşmamaktadır.")
        else:
            self.cursor.execute("INSERT INTO mfy_users (username,password) VALUES (?,?)", (self.regLine_user.text(),self.regLine_pw.text()))
            self.reg_label_status.setText(username.upper() + " Kullanıcısı Kaydı Yapılmıştır.")
            self.connect.commit()
            self.regLine_user.clear()
            self.regLine_pw.clear()
            self.regLine_repw.clear()

    def reg_clear(self):
        self.regLine_user.clear()
        self.regLine_pw.clear()
        self.regLine_repw.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    regWin = RegisterWindow()
    regWin.show()
    sys.exit(app.exec())