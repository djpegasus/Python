import sqlite3
import sys
from PyQt6.QtWidgets import QApplication,QMainWindow
from loginUI import Ui_loginForm
from opportunityMain import Opportunity
from registerMain import RegisterWindow

class Crm(QMainWindow,Ui_loginForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.crmdb()

        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)

    def crmdb(self):
        self.connect = sqlite3.connect("C:/Sqlite/CrmDB.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute("create table if not exists mfy_users (s_no INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
        self.connect.commit()

    def crmdbClose(self):
        self.connect.close()

    def register(self):
        self.regWindow = RegisterWindow()
        self.regWindow.show()

    def login(self):
        username = self.user_input.text()
        password = self.pw_input.text()
        self.cursor.execute("select * from mfy_users where username = ? and password = ?",(username,password))
        data = self.cursor.fetchall()
        if len(data) == 0:
            self.resultLabel.setText("Girilen Bilgiler Hatalı")
        else:
            if username == self.user_input.text() and password == self.pw_input.text():
                self.resultLabel.setText("Hoş Geldiniz "+ username)
                self.oppWin = Opportunity()
                self.oppWin.show()
                self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    crm = Crm()
    crm.show()
    sys.exit(app.exec())