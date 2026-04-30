import hashlib
import os
from pathlib import Path
import bcrypt
from encryption import Encryptor
from decryption import Decryptor
import sys
import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QFont, QColor, QPalette
from loginui import Loginui
from homeui import Mainpage
from PyQt6.QtWidgets import QMessageBox, QInputDialog
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
from ctypes import windll, byref, sizeof, c_int

def get_base_path():
    if getattr(sys, "frozen", False):
        base = Path(os.getenv("APPDATA")) / "AES_Encryptor"
    else:
        # Running from source (your IDE / terminal)
        base = Path("data/folder5")

    base.mkdir(parents=True, exist_ok=True)
    return base


BASE_DIR = get_base_path()
auth_path = BASE_DIR / "auth"


class UI(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AES-GCM Encryption Tool")
        self.setFixedSize(800, 200)
        self.setMinimumSize(0, 0)
        self.setWindowIcon(QIcon("materials/appicon.png"))

        self.encryptor = Encryptor()
        self.decryptor = Decryptor()
        auth_path.mkdir(parents=True, exist_ok=True)

        # Set white background, black text
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        # Page controls
        self.stack = qt.QStackedWidget()

        # login page
        self.page0 = qt.QWidget()
        self.login_ui = Loginui(auth_path)
        self.login_ui.loginui(self.page0, stack=self.stack)
        self.stack.addWidget(self.page0)

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
        #self.setFixedHeight(400)

    def showEvent(self, event):
        super().showEvent(event)
        HWND = int(self.winId())
        r1 = windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0xFFFFFF)), sizeof(c_int))
        r2 = windll.dwmapi.DwmSetWindowAttribute(HWND, 20, byref(c_int(0)), sizeof(c_int))
        windll.dwmapi.DwmSetWindowAttribute(HWND, 36, byref(c_int(0x000000)), sizeof(c_int))

    def checkpassword(self, passwrd):
        file = auth_path / "auth.dat"
        if not file.exists():
            return False
        temp = file.read_bytes()
        return bcrypt.checkpw(passwrd.encode(), temp)

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

        if not self.checkpassword(password):
            qt.QMessageBox.critical(self, "Error", "Password is wrong")
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

        if not self.checkpassword(password):
            qt.QMessageBox.critical(self, "Error", "Password is wrong")
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
