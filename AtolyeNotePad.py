from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


import os, sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)


        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(12)
        self.editor.setFont(font)

        self.path = None

        status = QStatusBar()
        self.setStatusBar(status)
        toolBar = QToolBar()
        toolBar.setIconSize(QSize(14,14))
        self.addToolBar(toolBar)


        menu_bar = self.menuBar()

        dosya_menu = menu_bar.addMenu("Dosya")
        ekle_menu = menu_bar.addMenu("Ekle")

        dosya_ac = QAction(QIcon(os.path.join("dosya_ac.png")), "Dosya Aç", self)
        dosya_ac.setStatusTip("Farklı Bir Text Dosyasını, AtolyeNotePad Dosyanıza Aktarmanızı Sağlar")
        dosya_menu.addAction(dosya_ac)
        toolBar.addAction(dosya_ac)
        dosya_ac.setShortcut("Ctrl+O")

        kaydet = QAction(QIcon(os.path.join("kaydet.png")), "Kaydet", self)
        kaydet.setStatusTip("Dosyanızı Varsayılan Dosyanın Üzerine Kaydetmenizi Sağlar")
        dosya_menu.addAction(kaydet)
        toolBar.addAction(kaydet)
        kaydet.setShortcut("Ctrl+S")
        
        farkli_kaydet = QAction(QIcon(os.path.join("farkli_kaydet.png")), "Farklı Kaydet", self)
        farkli_kaydet.setStatusTip("Dosyanızı İstediğiniz Dizine Kaydetmenizi Sağlar")
        dosya_menu.addAction(farkli_kaydet)
        toolBar.addAction(farkli_kaydet)
        
        yazdir = QAction(QIcon(os.path.join("yazdir.png")), "Yazdır", self)
        yazdir.setStatusTip("Dosyanızı Yazdırmanızı Sağlar")
        dosya_menu.addAction(yazdir)
        yazdir.setShortcut("Ctrl+P")

        geri_al = QAction(QIcon(os.path.join("geri_al.png")), "Geri Al", self)
        geri_al.setStatusTip("Dosya Üzerinde Yaptığınız Son İşlemi Geri Almanızı Sağlar")
        ekle_menu.addAction(geri_al)
        toolBar.addAction(geri_al)
        geri_al.setShortcut("Ctrl+Z")

        ileri_al = QAction(QIcon(os.path.join("ileri_al.png")), "İleri Al", self)
        ileri_al.setStatusTip("Dosya Üzerinde Geri Aldığınız Son İşlemi Tekrar Yapmanızı Sağlar")
        ekle_menu.addAction(ileri_al)
        toolBar.addAction(ileri_al)
        ileri_al.setShortcut("Ctrl+Y")

        kes = QAction(QIcon(os.path.join("kes.png")), "Kes", self)
        kes.setStatusTip("Dosya Üzerindeki Seçilen Kısımları Kesmenizi Sağlar")
        ekle_menu.addAction(kes)
        toolBar.addAction(kes)
        kes.setShortcut("Ctrl+X")

        kopyala = QAction(QIcon(os.path.join("kopyala.png")), "Kopyala", self)
        kopyala.setStatusTip("Dosya Üzerindeki Seçilen Kısımları Kopyalamanızı Sağlar")
        ekle_menu.addAction(kopyala)
        toolBar.addAction(kopyala)
        kopyala.setShortcut("Ctrl+C")

        yapistir = QAction(QIcon(os.path.join("yapistir.png")), "Yapıştır", self)
        yapistir.setStatusTip("Kopyalanan ya da Kesilen Öğeyi Dosya Üzerine Yapıştırır")
        ekle_menu.addAction(yapistir)
        toolBar.addAction(yapistir)
        yapistir.setShortcut("Ctrl+V")

        hepsini_sec = QAction(QIcon(os.path.join("hepsini_sec.png")), "Hepsini Seç", self)
        hepsini_sec.setStatusTip("Dosya Üzerindeki Tüm Verilerin Seçilmesini Sağlar")
        ekle_menu.addAction(hepsini_sec)
        toolBar.addAction(hepsini_sec)
        hepsini_sec.setShortcut("Ctrl+A")

        dosya_ac.triggered.connect(self.dosya_ac_def)
        kaydet.triggered.connect(self.kaydet_def)
        farkli_kaydet.triggered.connect(self.farkli_kaydet_def)
        yazdir.triggered.connect(self.yazdir_def)
        geri_al.triggered.connect(self.editor.undo)
        ileri_al.triggered.connect(self.editor.redo)
        kes.triggered.connect(self.editor.cut)
        kopyala.triggered.connect(self.editor.copy)
        yapistir.triggered.connect(self.editor.paste)
        hepsini_sec.triggered.connect(self.editor.selectAll)


        self.basligi_guncelle()
        self.setGeometry(100,100,500,500)
        self.show()
        
    def hata_mesaj(self, mesaj):
        hata = QMessageBox()
        hata.setText(mesaj)
        hata.setIcon(QMessageBox.Critical)
        hata.show()
        
        
    def basligi_guncelle(self):
        self.setWindowTitle("{} - AtolyeNotePad".format(os.path.basename(self.path) if self.path else "Untitled"))

    def dosya_ac_def(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Text Dosyaları (*.txt)")
        if path:
            try:
                with open(path, "r") as file:
                    text = file.read()
            except Exception as e:
                self.hata_mesaj(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.basligi_guncelle()



    def kaydet_def(self):
        if self.path is None:
            return self.farkli_kaydet_def()

        text = self.editor.toPlainText()

        try:
            with open(self.path, "w") as file:

                file.write(text)
        except Exception as e:
            self.hata_mesaj(str(e))


    def farkli_kaydet_def(self):
        path, _ = QFileDialog.getSaveFileName(self, "Farklı Kaydet", "", "Text Dosyası (*.txt)")

        if not path:
            return

        text = self.editor.toPlainText()

        try:
            with open(path, "w") as file:

                file.write(text)
                self.path = path
                self.basligi_guncelle()
        except Exception as e:
            self.hata_mesaj(str(e))


    def yazdir_def(self):
        mesaj = QPrintDialog()
        if mesaj.exec_():
            self.editor.print_(mesaj.printer())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("AtolyeNotePad")


    window = MainWindow()
    app.exec_()
