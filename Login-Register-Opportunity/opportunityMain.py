from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from opportunityUI import Ui_MainWindow
import pandas as pd
import sqlite3
import sys

class Opportunity(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.crmdb()

        self.loadButton.clicked.connect(self.loadFile)
        self.saveButton.clicked.connect(self.saveFile)

    def crmdb(self):
        self.connect = sqlite3.connect("C:/Sqlite/CrmDB.db")
        self.cursor = self.connect.cursor()
        self.cursor.execute("create table if not exists mfy_opp (firsat_adi TEXT, firma_adi TEXT, sip_kodu TEXT, firsat_tutar INT, "
                            "doviz_cins TEXT, kapanis_tarihi DATE, status TEXT, sa_tutari INT, kar INT, aciklama TEXT)")
        self.connect.commit()

    def crmdbClose(self):
        self.connect.close()

    def loadFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Excel Dosyasını Seç", "", "Excel Files (*.xlsx *.xls)")

        if file_path:
            # Excel dosyasını pandas ile yükle
            self.df = pd.read_excel(file_path)

            # DataFrame'i tabloya aktar
            self.table_widget.setRowCount(self.df.shape[0])
            self.table_widget.setColumnCount(self.df.shape[1])
            self.table_widget.setHorizontalHeaderLabels(self.df.columns)

            for row in range(self.df.shape[0]):
                for col in range(self.df.shape[1]):
                    value = str(self.df.iat[row, col])
                    self.table_widget.setItem(row, col, QTableWidgetItem(value))

    def saveFile(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    opp = Opportunity()
    opp.show()
    sys.exit(app.exec())