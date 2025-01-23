from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from uiCariInterface import Ui_Form
import sys
import sqlite3

class CariInf(QMainWindow,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.database()
        self.loadData()
        self.tablerow = 0

        self.saveButton.clicked.connect(self.cariRegister)
        self.clearButton.clicked.connect(self.clearArea)
        self.refresh.clicked.connect(self.refreshButton)
        self.silButton.clicked.connect(self.delete)

    def database(self):
        self.connect = sqlite3.connect("c:/Sqlite/caridb.db")
        self.cursor = self.connect.cursor()
        sorgu = "create table if not exists cari (c_kodu TEXT, c_adi TEXT, sektor TEXT, doviz TEXT, vade TEXT, asatis TEXT, isatis TEXT, satinalma TEXT, email TEXT, adres TEXT, il TEXT, ilce TEXT, ulke TEXT, m_mail TEXT, tel TEXT, mobil TEXT, fax TEXT, vergi_d TEXT, vergi_no TEXT, banka TEXT, iban TEXT)"
        self.cursor.execute(sorgu)
        self.connect.commit()

    def close(self):
        self.connect.close()

    def cariRegister(self):
        self.cursor.execute("insert into cari (c_kodu,c_adi,sektor, doviz, vade, asatis, isatis, satinalma, email, adres, il, ilce, ulke, m_mail, tel, mobil, fax, vergi_d, vergi_no, banka, iban) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            (self.ckodu_line.text(),self.cadi_line.text(),self.csektor_line.text(),self.dc_box.currentText(),self.vade_line.text(),self.asatis_line.text(),self.isatis_line.text(),
                             self.satinalma_line.text(),self.email_line.text(),self.addr_line.text(),self.province_line.text(),self.district_line.text(),self.country_line.text(),
                             self.mmail_line.text(),self.tel_line.text(),self.mobil_line.text(),self.fax_line.text(),self.vd_line.text(),self.vno_line.text(),self.bank_line.text(),self.iban_line.text()))
        self.result.setText("Kayıt Başarılı.")
        self.connect.commit()

    def clearArea(self):
        self.ckodu_line.clear(),self.cadi_line.clear(),self.csektor_line.clear(),self.vade_line.clear(),self.asatis_line.clear(),self.isatis_line.clear(),
        self.satinalma_line.clear(),self.email_line.clear(),self.addr_line.clear(),self.province_line.clear(),self.district_line.clear(),self.country_line.clear(),
        self.mmail_line.clear(),self.tel_line.clear(),self.mobil_line.clear(),self.fax_line.clear(),self.vd_line.clear(),self.vno_line.clear(),self.bank_line.clear(),self.iban_line.clear()
        self.result.setText("Ekran Temizlendi.")

    def loadData(self):
        sorgu = "select c_kodu, c_adi, sektor, doviz, vade, asatis, isatis, satinalma, email, mobil from cari limit 50 "
        self.tablerow = 0
        data = self.cursor.execute(sorgu)
        self.tableWidget.setRowCount(50)
        for row in data:
            self.tableWidget.setItem(self.tablerow, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(self.tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(self.tablerow, 2, QTableWidgetItem(row[2]))
            self.tableWidget.setItem(self.tablerow, 3, QTableWidgetItem(row[3]))
            self.tableWidget.setItem(self.tablerow, 5, QTableWidgetItem(row[5]))
            self.tableWidget.setItem(self.tablerow, 6, QTableWidgetItem(row[6]))
            self.tableWidget.setItem(self.tablerow, 7, QTableWidgetItem(row[7]))
            self.tableWidget.setItem(self.tablerow, 8, QTableWidgetItem(row[8]))
            self.tableWidget.setItem(self.tablerow, 9, QTableWidgetItem(row[9]))
            self.tablerow += 1

    def refreshButton(self):
        self.loadData()

    def delete(self):
        sender = self.sender()
        if sender:
            row = self.tableWidget.indexAt(sender.pos()).row()
            self.tableWidget.removeRow(row)
            sorgu = "delete "



if __name__ == "__main__":
    app = QApplication(sys.argv)
    cari = CariInf()
    cari.show()
    sys.exit(app.exec())

