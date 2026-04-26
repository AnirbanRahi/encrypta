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

auth_path = Path("data/folder5")

class UI(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AES-GCM Encryption Tool")
        self.resize(800, 400)

        self.encryptor = Encryptor()
        self.decryptor = Decryptor()

        # Set white background, black text
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        # Page controls
        self.stack = qt.QStackedWidget()

        # login page
        self.page0 = qt.QWidget()
        self.login_ui = Loginui()
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

    def checkpassword(self, passwrd):
        dir = auth_path
        file = dir / "auth.dat"
        temp = file.read_bytes()
        return bcrypt.checkpw(passwrd.encode(), temp)

    # Encryption
    def encryptfile(self, path):
        if not path:
            qt.QMessageBox.critical(self, "Error", "No file or folder selected for encryption")
            return

        string_path = Path(path)

        if not string_path.exists():
            qt.QMessageBox.critical(self, "Error", "Selected path does not exist")
            return

        if string_path.name.endswith(".enc"):
            qt.QMessageBox.critical(self, "Error", "This file is already encrypted.")
            return

        password, ok = qt.QInputDialog.getText(self, "Ask Password", "Enter Master Password:")

        if not ok or not password or len(password) < 3:
            qt.QMessageBox.critical(self, "Error", "Password must be at least 3 characters")
            return

        if not self.checkpassword(password):
            qt.QMessageBox.critical(self, "Error", "Master Password Wrong")
            return

        try:
            newfile = self.encryptor.encrypt(path, password)
            qt.QMessageBox.information(self, "Success", f"Encrypted: {newfile}")
        except Exception as e:
            qt.QMessageBox.critical(self, "Error", str(e))

    #  Decryption
    def decryptfile(self, path):
        if not path:
            qt.QMessageBox.critical(self, "Error", "No file or folder selected for decryption")
            return

        string_path = Path(path)

        if not string_path.exists():
            qt.QMessageBox.critical(self, "Error", "Selected path does not exist")
            return

        if not string_path.name.endswith(".enc"):
            qt.QMessageBox.critical(self, "Error", "This file is not encrypted.")
            return

        password, ok = qt.QInputDialog.getText(self, "Ask Password", "Enter Master Password:")
        if not ok or not password or len(password) < 3:
            qt.QMessageBox.critical(self, "Error", "Password must be at least 3 characters")
            return

        if not self.checkpassword(password):
            qt.QMessageBox.critical(self, "Error", "Master Password Wrong")
            return

        try:
            newfile = self.decryptor.decrypt(path,password)
            qt.QMessageBox.information(self, "Success", f"Decrypted: {newfile}")
        except Exception as e:
            qt.QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())
