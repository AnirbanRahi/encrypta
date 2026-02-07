import hashlib
import os
from pathlib import Path

from PyQt6 import sip
import bcrypt
from encryption import Encryptor
from decryption import Decryptor
import sys
import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt
from styles import *
from PyQt6.QtWidgets import QStackedWidget, QLineEdit

auth_path = Path("data/folder5")
key_path = Path("data/folder5")


class UI(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AES-GCM Encryption Tool")
        self.resize(800, 400)

        self.encryptor = Encryptor()
        self.decryptor = Decryptor(key_dir=key_path)
        self.filepathenc = ""
        self.filepathdec = ""

        # key
        self.key_file()

        # Active mode flags
        self.enc_mode = "file"
        self.passwordstored = ""
        # GUI elements
        self.lineenc = None
        self.linedec = None

        self.enc_folder_btn = None
        self.dec_file_btn = None
        self.enc_file_btn = None

        # Set white background, black text
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))
        self.setPalette(palette)

        # Page controls
        self.stack = QStackedWidget()

        self.page0 = qt.QWidget()
        self.loginui(self.page0)
        self.stack.addWidget(self.page0)

        self.page1 = qt.QWidget()
        self.setupui(self.page1)
        self.stack.addWidget(self.page1)

        main_layout = qt.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Add this line
        main_layout.setSpacing(0)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def loginui(self, widget):

        font_button = QFont("Arial", 16)

        full_layout = qt.QHBoxLayout()
        full_layout.setSpacing(20)
        full_layout.setContentsMargins(0, 0, 0, 0)

        # image
        picwidget = qt.QWidget()
        piclayout = qt.QVBoxLayout()
        piclayout.setContentsMargins(0, 0, 0, 0)
        piclayout.setSpacing(0)
        logpicture = qt.QLabel()
        logpicture.setContentsMargins(0, 0, 0, 0)
        pixmap = QPixmap("materials/login2.jpg")
        pixmap = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logpicture.setPixmap(pixmap)
        logpicture.setScaledContents(True)
        piclayout.addWidget(logpicture)
        picwidget.setLayout(piclayout)

        # form
        formwidget = qt.QWidget()
        formlayout = qt.QVBoxLayout()
        formlayout.setContentsMargins(0, 0, 0, 0)
        formlayout.setSpacing(20)

        passwordset = self.checkdir()

        passline = QLineEdit()
        passline.setPlaceholderText("Enter Password")
        passline.setStyleSheet(line_style)

        if not passwordset:
            setlogbutton = qt.QPushButton("Set Password")
            setlogbutton.setStyleSheet("color: black; font-size: 20px;")
            button = qt.QPushButton("Set Password")
            button.setFont(font_button)
            button.setStyleSheet(enc_dec_button)
            button.clicked.connect(self.setpassword)
            passline.clear()

        else:
            setlogbutton = qt.QPushButton("Login")
            setlogbutton.setStyleSheet("color: black; font-size: 20px;")
            button = qt.QPushButton("Login")
            button.setFont(font_button)
            button.setStyleSheet(enc_dec_button)
            button.clicked.connect(lambda: self.handle_login(passline))

        formlayout.addStretch()
        formlayout.addWidget(setlogbutton)
        formlayout.addWidget(passline)
        formlayout.addWidget(button)
        formlayout.addStretch()
        formwidget.setLayout(formlayout)

        full_layout.addWidget(picwidget, 1)
        full_layout.addWidget(formwidget, 1)

        widget.setLayout(full_layout)

    def checkpassword(self, passwrd):
        dir = auth_path
        file = dir / "auth.dat"
        temp = file.read_bytes()
        return bcrypt.checkpw(passwrd.encode(), temp)

    def setpassword(self):
        passline = self.page0.findChild(QLineEdit)
        password = passline.text().strip()
        if not password:
            qt.QMessageBox.critical(self, "Error", "Password cannot be empty")
            return

        # Save the password
        dir = auth_path
        dir.mkdir(parents=True, exist_ok=True)
        file = dir / "auth.dat"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        file.write_bytes(hashed)

        # Rebuild login UI for entering the password
        # First clear old layout
        old_layout = self.page0.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            sip.delete(old_layout)

        self.loginui(self.page0)
        self.stack.setCurrentIndex(0)

        qt.QMessageBox.information(self, "Success", "Password saved! Please login now.")

    def handle_login(self, passline):
        password = passline.text().strip()
        if not password:
            qt.QMessageBox.critical(self, "Error", "Password cannot be empty")
            return
        if self.checkpassword(password):
            self.stack.setCurrentIndex(1)
        else:
            qt.QMessageBox.critical(self, "Error", "Wrong password")
            passline.clear()

    def checkdir(self):
        dir = auth_path
        file = dir / "auth.dat"
        if not dir.exists():
            dir.mkdir(parents=True, exist_ok=True)

        if not file.exists():
            return False
        else:
            return True

    def setupui(self, widget):
        font_header = QFont("Arial", 14, QFont.Weight.Bold)
        font_button = QFont("Arial", 11)

        main_layout = qt.QVBoxLayout()
        main_layout.setSpacing(20)

        # Encryption Section
        enc_label = qt.QLabel("Encryption")
        enc_label.setFont(font_header)
        main_layout.addWidget(enc_label)

        # Mode buttons
        enc_mode_layout = qt.QHBoxLayout()
        self.enc_file_btn = qt.QPushButton("Encrypt File")
        self.enc_folder_btn = qt.QPushButton("Encrypt Folder")
        self.enc_file_btn.setCheckable(True)
        self.enc_folder_btn.setCheckable(True)
        self.enc_file_btn.setFont(font_button)
        self.enc_folder_btn.setFont(font_button)
        self.enc_file_btn.setChecked(True)
        self.update_enc_mode_style()

        self.enc_file_btn.clicked.connect(lambda: self.set_enc_mode("file"))
        self.enc_folder_btn.clicked.connect(lambda: self.set_enc_mode("folder"))

        enc_mode_layout.addWidget(self.enc_file_btn)
        enc_mode_layout.addWidget(self.enc_folder_btn)
        main_layout.addLayout(enc_mode_layout)

        # Browse and path
        enc_browse_layout = qt.QHBoxLayout()
        self.lineenc = qt.QLineEdit()
        self.lineenc.setPlaceholderText("Select file or folder to encrypt")
        self.lineenc.setStyleSheet(line_style)
        browse_btn_enc = qt.QPushButton("Browse")
        browse_btn_enc.setFont(font_button)
        browse_btn_enc.setStyleSheet(inactive_button)
        browse_btn_enc.clicked.connect(self.file_or_folder_enc)
        enc_browse_layout.addWidget(self.lineenc)
        enc_browse_layout.addWidget(browse_btn_enc)
        main_layout.addLayout(enc_browse_layout)

        # Encrypt button
        enc_action_btn = qt.QPushButton("Encrypt")
        enc_action_btn.setFont(font_button)
        enc_action_btn.setStyleSheet(enc_dec_button)
        enc_action_btn.clicked.connect(self.encryptfile)
        main_layout.addWidget(enc_action_btn)

        # Decryption Section
        dec_label = qt.QLabel("Decryption")
        dec_label.setFont(font_header)
        main_layout.addWidget(dec_label)

        # Mode buttons
        dec_mode_layout = qt.QHBoxLayout()
        self.dec_file_btn = qt.QPushButton("Decrypt File")
        self.dec_file_btn.setFont(font_button)
        self.dec_file_btn.setCheckable(True)
        self.dec_file_btn.setChecked(True)
        self.dec_file_btn.setStyleSheet(inactive_button)
        dec_mode_layout.addWidget(self.dec_file_btn)
        main_layout.addLayout(dec_mode_layout)

        # Browse and path
        dec_browse_layout = qt.QHBoxLayout()
        self.linedec = qt.QLineEdit()
        self.linedec.setPlaceholderText("Select file to decrypt")
        self.linedec.setStyleSheet(line_style)
        browse_btn_dec = qt.QPushButton("Browse")
        browse_btn_dec.setFont(font_button)
        browse_btn_dec.clicked.connect(self.file_dec)
        browse_btn_dec.setStyleSheet(inactive_button)
        dec_browse_layout.addWidget(self.linedec)
        dec_browse_layout.addWidget(browse_btn_dec)
        main_layout.addLayout(dec_browse_layout)

        # Decrypt button
        dec_action_btn = qt.QPushButton("Decrypt")
        dec_action_btn.setStyleSheet(enc_dec_button)
        dec_action_btn.setFont(font_button)
        dec_action_btn.clicked.connect(self.decryptfile)
        main_layout.addWidget(dec_action_btn)

        widget.setLayout(main_layout)

    #  Mode styling
    def set_enc_mode(self, mode):
        self.enc_mode = mode
        self.update_enc_mode_style()
        self.lineenc.clear()
        self.filepathenc = ""

    def update_enc_mode_style(self):
        if self.enc_mode == "file":
            self.enc_file_btn.setStyleSheet(active_button)
            self.enc_folder_btn.setStyleSheet(inactive_button)
        else:
            self.enc_file_btn.setStyleSheet(inactive_button)
            self.enc_folder_btn.setStyleSheet(active_button)

    # Browse
    def file_or_folder_enc(self):
        if self.enc_mode == "file":
            path, _ = qt.QFileDialog.getOpenFileName(self, "Select File")
        else:
            path = qt.QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.filepathenc = str(path)
            self.lineenc.setText(self.filepathenc)

    def file_dec(self):
        path, _ = qt.QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.filepathdec = str(path)
            self.linedec.setText(self.filepathdec)

    # magic key
    def key_file(self):
        key_path.mkdir(parents=True, exist_ok=True)
        existing = list(key_path.glob("key*.dat"))

        if existing:
            # Use the first key found
            keyfile = max(existing, key=lambda f: f.stat().st_mtime)
            with open(keyfile, "rb") as f:
                lines = f.read().split(b"\n", 1)
                magic_code = lines[0].decode()
                key_bytes = lines[1]
            self.current_key = (magic_code, key_bytes)
            return keyfile
        else:
            # generate 32-byte AES key
            key_bytes = os.urandom(32)

            # generate magic code
            magic_code = os.urandom(16)

            keyfile = key_path / "key1.dat"
            with open(keyfile, "wb") as f:
                f.write(magic_code)
                f.write(key_bytes)

            self.current_key = (magic_code, key_bytes)
            return keyfile

    # Encryption
    def encryptfile(self):
        if not self.filepathenc:
            qt.QMessageBox.critical(self, "Error", "No file or folder selected for encryption")
            return

        string_path = Path(self.filepathenc)
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
            magcode, key = self.current_key
            newfile = self.encryptor.encrypt(self.filepathenc, magcode, key)
            qt.QMessageBox.information(self, "Success", f"Encrypted: {newfile}")
        except Exception as e:
            qt.QMessageBox.critical(self, "Error", str(e))

    #  Decryption
    def decryptfile(self):
        if not self.filepathdec:
            qt.QMessageBox.critical(self, "Error", "No file or folder selected for decryption")
            return
        string_path = Path(self.filepathdec)
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
            newfile = self.decryptor.decrypt(self.filepathdec)
            qt.QMessageBox.information(self, "Success", f"Decrypted: {newfile}")
        except Exception as e:
            qt.QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = qt.QApplication(sys.argv)
    window = UI()
    window.checkdir()
    window.show()
    sys.exit(app.exec())
