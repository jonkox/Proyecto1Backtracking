import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(500, 500)

        self.setWindowTitle("Hola mundo")

app = QApplication(sys.argv)
ventanita = VentanaPrincipal()
ventanita.show()
sys.exit(app.exec())