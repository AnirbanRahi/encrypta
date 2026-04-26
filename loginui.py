from pathlib import Path

from PyQt6 import sip
import bcrypt
import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
from PyQt6.QtCore import Qt
from styles import *
from PyQt6.QtWidgets import QStackedWidget, QLineEdit

auth_path = Path("data/folder5")

class Loginui:

    def loginui(self, parent: qt.QWidget, stack: QStackedWidget):
        self.parent = parent
        self.stack = stack

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
        passline = self.parent.findChild(QLineEdit)
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

        parent.setLayout(full_layout)

    def checkpassword(self, passwrd):
        dir = auth_path
        file = dir / "auth.dat"
        temp = file.read_bytes()
        return bcrypt.checkpw(passwrd.encode(), temp)

    def setpassword(self):
        passline = self.parent.findChild(QLineEdit)
        password = passline.text().strip()
        if not password:
            qt.QMessageBox.critical(self.parent, "Error", "Password cannot be empty")
            return

        # Save the password
        dir = auth_path
        dir.mkdir(parents=True, exist_ok=True)
        file = dir / "auth.dat"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        file.write_bytes(hashed)

        # Rebuild login UI for entering the password
        # First clear old layout
        old_layout = self.parent.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            sip.delete(old_layout)

        self.loginui(self.parent, self.stack)
        self.stack.setCurrentIndex(0)

        qt.QMessageBox.information(self.parent, "Success", "Password saved! Please login now.")

    def handle_login(self, passline):
        password = passline.text().strip()
        if not password:
            qt.QMessageBox.critical(self.parent, "Error", "Password cannot be empty")
            return
        if self.checkpassword(password):
            self.stack.setCurrentIndex(1)
        else:
            qt.QMessageBox.critical(self.parent, "Error", "Wrong password")
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
