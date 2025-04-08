import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.dashboard import Dashboard
from utils.icone import usar_icone

def main():
    app = QApplication(sys.argv)

    usar_icone(app)

    with open("styles/main.qss", "r") as file:
        app.setStyleSheet(file.read())

    janela = Dashboard()
    janela.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
