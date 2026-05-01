import hashlib
import os
from pathlib import Path
import bcrypt
from encryption import Encryptor
from decryption import Decryptor
import sys
import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QFont, QColor, QPalette
from homeui import Mainpage
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
from ctypes import windll, byref, sizeof, c_int

def resource_path(path):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, path)

class UI(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Encrypta")
        self.setFixedSize(800, 400)
        self.setMinimumSize(0, 0)
        self.setWindowIcon(QIcon(resource_path("materials/appicon.png")))

        self.encryptor = Encryptor()
        self.decryptor = Decryptor()

        # Set white background, black text
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        # Page controls
        self.stack = qt.QStackedWidget()

        # home page
        self.page1 = qt.QWidget()
        self.main_ui = Mainpage()
        self.main_ui.mainpage(self.encryptfile, self.decryptfile, parent=self.page1, stack=self.stack)
        self.stack.addWidget(self.page1)

        main_layout = qt.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def showEvent(self, event):
        super().showEvent(event)
        HWND = int(self.winId())
        r1 = windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0xFFFFFF)), sizeof(c_int))
        r2 = windll.dwmapi.DwmSetWindowAttribute(HWND, 20, byref(c_int(0)), sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(0x000000)), sizeof(c_int))

    # Encryption
    def encryptfile(self, path, password):
        if not path:
            qt.QMessageBox.critical(self, "Error", "No file or folder selected for encryption")
            return False

        string_path = Path(path)

        if not string_path.exists():
            qt.QMessageBox.critical(self, "Error", "Selected path does not exist")
            return False

        if string_path.name.endswith(".enc"):
            qt.QMessageBox.critical(self, "Error", "This file is already encrypted.")
            return False

        if not password or len(password) < 3:
            qt.QMessageBox.critical(self, "Error", "Password must be at least 3 characters")
            return False

        try:
            newfile = self.encryptor.encrypt(path, password)
            qt.QMessageBox.information(self, "Success", f"Encrypted: {newfile}")
            return True
        except Exception as e:
            qt.QMessageBox.critical(self, "Error", str(e))
            return False

    #  Decryption
    def decryptfile(self, path, password):
        if not path:
            qt.QMessageBox.critical(self, "Error", "No file or folder selected for decryption")
            return False

        string_path = Path(path)

        if not string_path.exists():
            qt.QMessageBox.critical(self, "Error", "Selected path does not exist")
            return False

        if not string_path.name.endswith(".enc"):
            qt.QMessageBox.critical(self, "Error", "This file is not encrypted.")
            return False

        if not password or len(password) < 3:
            qt.QMessageBox.critical(self, "Error", "Password must be at least 3 characters")
            return False

        try:
            newfile = self.decryptor.decrypt(path, password)
            qt.QMessageBox.information(self, "Success", f"Decrypted: {newfile}")
            return  True
        except Exception as e:
            qt.QMessageBox.critical(self, "Error", str(e))
            return False


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())
