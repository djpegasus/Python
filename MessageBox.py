from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QVBoxLayout
import sys
class SilmePenceresi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Satır Silme")
        self.setGeometry(100, 100, 300, 150)

        # Ana layout
        layout = QVBoxLayout()

        # Satır numarası girişi için QLineEdit
        self.satir_input = QLineEdit(self)
        self.satir_input.setPlaceholderText("Silmek istediğiniz satır numarasını girin")
        layout.addWidget(self.satir_input)

        # Silme butonu
        self.sil_button = QPushButton("Sil", self)
        self.sil_button.clicked.connect(self.silme_islemi)
        layout.addWidget(self.sil_button)

        # Layout'u pencereye yerleştir
        self.setLayout(layout)

    def silme_islemi(self):
        # Kullanıcıdan alınan satır numarasını al
        satir_numarasi = self.satir_input.text()

        if not satir_numarasi.isdigit():  # Eğer kullanıcı geçerli bir sayısal değer girmezse
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir satır numarası girin.")
            return

        # Silme işlemi için onay mesaj kutusu
        cevap = QMessageBox.question(
            self,
            "Silme Onayı",
            f"{satir_numarasi}. satırı silmek istediğinizden emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if cevap == QMessageBox.StandardButton.Yes:
            # Gerçek silme işlemi burada yapılır (örneğin bir dosya veya liste üzerinde)
            QMessageBox.information(self, "Başarılı", f"{satir_numarasi}. satır başarıyla silindi.")
        else:
            QMessageBox.information(self, "İptal", "Silme işlemi iptal edildi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cari = SilmePenceresi()
    cari.show()
    sys.exit(app.exec())