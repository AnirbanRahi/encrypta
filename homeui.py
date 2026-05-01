import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap, QIcon
from styles import *
from PyQt6.QtWidgets import QStackedWidget, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon


class Mainpage(qt.QWidget):
    def mainpage(self, encryptfile, decryptfile, parent: qt.QWidget, stack=QStackedWidget):
        self.parent = parent
        self.stack = stack
        self.encryptfile = encryptfile
        self.decryptfile = decryptfile
        self.buttonwidth = 60
        self.height = 40
        self.iconsize = 22
        self.ffbutton=30

        font_header = QFont("Arial", 14, QFont.Weight.Bold)
        font_button = QFont("Arial", 11)

        main_layout = qt.QHBoxLayout()
        main_layout.setSpacing(25)


        #image
        picture = qt.QLabel()
        pixmap = QPixmap("materials/pic.png")
        if pixmap.isNull():
            print("Image failed to load")
        pixmap = pixmap.scaled(
            350,
            350,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        picture.setPixmap(pixmap)
        picture.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Encryption Section
        enc_layout = qt.QVBoxLayout()
        enc_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        enc_header_layout = qt.QHBoxLayout()
        iconenc = qt.QLabel()
        iconenc.setPixmap(QPixmap("materials/encicon.png").scaled(24, 24))
        enc_label = qt.QLabel("Encryption")
        enc_label.setFont(font_header)
        enc_header_layout.addWidget(iconenc)
        enc_header_layout.addWidget(enc_label)
        enc_header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        enc_layout.addLayout(enc_header_layout)

        # Mode buttons
        enc_mode_layout = qt.QHBoxLayout()
        self.enc_file_btn = qt.QPushButton("Encrypt File")
        self.enc_file_btn.setFixedHeight(self.ffbutton)
        self.enc_folder_btn = qt.QPushButton("Encrypt Folder")
        self.enc_folder_btn.setFixedHeight(self.ffbutton)
        self.enc_file_btn.setCheckable(True)
        self.enc_folder_btn.setCheckable(True)
        self.enc_file_btn.setFont(font_button)
        self.enc_folder_btn.setFont(font_button)
        self.enc_file_btn.setChecked(True)
        self.enc_mode = "file"
        self.update_enc_mode_style()

        self.enc_file_btn.clicked.connect(lambda: self.set_enc_mode("file"))
        self.enc_folder_btn.clicked.connect(lambda: self.set_enc_mode("folder"))

        enc_mode_layout.addWidget(self.enc_file_btn)
        enc_mode_layout.addWidget(self.enc_folder_btn)
        enc_layout.addLayout(enc_mode_layout)

        # Browse and path
        enc_browse_layout = qt.QHBoxLayout()
        enc_browse_layout.setSpacing(0)
        self.lineenc = qt.QLineEdit()
        self.lineenc.setFixedHeight(self.height)
        self.lineenc.setPlaceholderText("Select file or folder to encrypt")
        self.lineenc.setStyleSheet(line_style)

        iconbrowseenc = qt.QPushButton()
        iconbrowseenc.setIcon(QIcon("materials/folder.png"))
        iconbrowseenc.setFixedWidth(self.buttonwidth)
        iconbrowseenc.setStyleSheet(icons)
        iconbrowseenc.setFixedHeight(self.height)
        iconbrowseenc.setIconSize(QSize(self.iconsize, self.iconsize))
        iconbrowseenc.clicked.connect(self.file_or_folder_enc)

        enc_browse_layout.addWidget(self.lineenc)
        enc_browse_layout.addWidget(iconbrowseenc)
        enc_layout.addLayout(enc_browse_layout)

        # Encryption Password
        enc_pass_layout = qt.QHBoxLayout()
        enc_pass_layout.setSpacing(0)
        self.enc_password = qt.QLineEdit()
        self.enc_password.setFixedHeight(self.height)
        self.enc_password.setPlaceholderText("Enter encryption password")
        self.enc_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.enc_password.setStyleSheet(line_style)
        self.enc_password.setClearButtonEnabled(True)

        self.enc_toggle_btn = qt.QPushButton()
        self.enc_toggle_btn.setCheckable(True)
        self.enc_toggle_btn.setFixedWidth(self.buttonwidth)
        self.enc_toggle_btn.setIcon(QIcon("materials/invisible.png"))
        self.enc_toggle_btn.setFixedHeight(self.height)
        self.enc_toggle_btn.setIconSize(QSize(self.iconsize, self.iconsize))
        self.enc_toggle_btn.setStyleSheet(icons)
        self.enc_toggle_btn.clicked.connect(self.toggle_enc_password)

        enc_pass_layout.addWidget(self.enc_password)
        enc_pass_layout.addWidget(self.enc_toggle_btn)
        enc_layout.addLayout(enc_pass_layout)

        # Encrypt button
        enc_action_btn = qt.QPushButton("Encrypt")
        enc_action_btn.setFont(font_button)
        enc_action_btn.setStyleSheet(enc_dec_button)
        enc_action_btn.clicked.connect(
            lambda _: self.handle_encrypt()
        )
        enc_layout.addWidget(enc_action_btn)

        main_layout.addLayout(enc_layout)

        # Decryption Section
        dec_layout = qt.QVBoxLayout()
        dec_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        dec_header_layout = qt.QHBoxLayout()
        icondec = qt.QLabel()
        icondec.setPixmap(QPixmap("materials/decicon.png").scaled(24, 24))
        dec_label = qt.QLabel("Decryption")
        dec_label.setFont(font_header)
        dec_header_layout.addWidget(icondec)
        dec_header_layout.addWidget(dec_label)
        dec_header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        dec_layout.addLayout(dec_header_layout)

        # Mode buttons
        dec_mode_layout = qt.QHBoxLayout()
        self.dec_file_btn = qt.QPushButton("Decrypt File")
        self.dec_file_btn.setFixedHeight(self.ffbutton)
        self.dec_file_btn.setFont(font_button)
        self.dec_file_btn.setCheckable(True)
        self.dec_file_btn.setChecked(True)
        self.dec_file_btn.setStyleSheet(active_button)
        dec_mode_layout.addWidget(self.dec_file_btn)
        dec_layout.addLayout(dec_mode_layout)

        # Browse and path
        dec_browse_layout = qt.QHBoxLayout()
        dec_browse_layout.setSpacing(0)
        self.linedec = qt.QLineEdit()
        self.linedec.setFixedHeight(self.height)
        self.linedec.setPlaceholderText("Select file to decrypt")
        self.linedec.setStyleSheet(line_style)

        iconbrowsedec = qt.QPushButton()
        iconbrowsedec.setIcon(QIcon("materials/folder.png"))
        iconbrowsedec.setFixedWidth(self.buttonwidth)
        iconbrowsedec.setFixedHeight(self.height)
        iconbrowsedec.setStyleSheet(icons)
        iconbrowsedec.setIconSize(QSize(self.iconsize, self.iconsize))
        iconbrowsedec.clicked.connect(self.file_dec)

        dec_browse_layout.addWidget(self.linedec)
        dec_browse_layout.addWidget(iconbrowsedec)

        dec_layout.addLayout(dec_browse_layout)

        # Decryption Password
        dec_pass_layout = qt.QHBoxLayout()
        dec_pass_layout.setSpacing(0)
        self.dec_password = qt.QLineEdit()
        self.dec_password.setFixedHeight(self.height)
        self.dec_password.setPlaceholderText("Enter decryption password")
        self.dec_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.dec_password.setStyleSheet(line_style)
        self.dec_password.setClearButtonEnabled(True)

        self.dec_toggle_btn = qt.QPushButton()
        self.dec_toggle_btn.setCheckable(True)
        self.dec_toggle_btn.setFixedWidth(self.buttonwidth)
        self.dec_toggle_btn.setFixedHeight(self.height)
        self.dec_toggle_btn.setIcon(QIcon("materials/invisible.png"))
        self.dec_toggle_btn.setIconSize(QSize(self.iconsize, self.iconsize))
        self.dec_toggle_btn.setStyleSheet(icons)
        self.dec_toggle_btn.clicked.connect(self.toggle_dec_password)

        dec_pass_layout.addWidget(self.dec_password)
        dec_pass_layout.addWidget(self.dec_toggle_btn)
        dec_layout.addLayout(dec_pass_layout)

        # Decrypt button
        dec_action_btn = qt.QPushButton("Decrypt")
        dec_action_btn.setStyleSheet(enc_dec_button)
        dec_action_btn.setFont(font_button)
        dec_action_btn.clicked.connect(
            lambda _: self.handle_decrypt()
        )

        dec_layout.addWidget(dec_action_btn)

        main_layout.addLayout(dec_layout)

        outer = qt.QVBoxLayout()
        outer.addStretch()
        outer.addWidget(picture, alignment=Qt.AlignmentFlag.AlignCenter)
        outer.addLayout(main_layout)
        outer.addStretch()

        parent.setLayout(outer)

    def set_enc_mode(self, mode):
        self.enc_mode = mode
        self.update_enc_mode_style()
        self.lineenc.clear()

    def update_enc_mode_style(self):
        if self.enc_mode == "file":
            self.enc_file_btn.setStyleSheet(active_button)
            self.enc_folder_btn.setStyleSheet(inactive_button)
        else:
            self.enc_file_btn.setStyleSheet(inactive_button)
            self.enc_folder_btn.setStyleSheet(active_button)

    def handle_encrypt(self):
        success = self.encryptfile(self.lineenc.text(), self.enc_password.text())

        if success:
            self.lineenc.clear()
            self.enc_password.clear()
            self.enc_toggle_btn.setChecked(False)
            self.enc_toggle_btn.setIcon(QIcon("materials/invisible.png"))
            self.enc_password.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_decrypt(self):
        success = self.decryptfile(self.linedec.text(), self.dec_password.text())

        if success:
            self.linedec.clear()
            self.dec_password.clear()

            self.dec_toggle_btn.setChecked(False)
            self.dec_toggle_btn.setIcon(QIcon("materials/invisible.png"))
            self.dec_password.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_enc_password(self):
        if self.enc_toggle_btn.isChecked():
            self.enc_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.enc_toggle_btn.setIcon(QIcon("materials/visible.png"))
        else:
            self.enc_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.enc_toggle_btn.setIcon(QIcon("materials/invisible.png"))

    def toggle_dec_password(self):
        if self.dec_toggle_btn.isChecked():
            self.dec_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.dec_toggle_btn.setIcon(QIcon("materials/visible.png"))
        else:
            self.dec_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.dec_toggle_btn.setIcon(QIcon("materials/invisible.png"))

    # Browse
    def file_or_folder_enc(self):
        if self.enc_mode == "file":
            path, _ = qt.QFileDialog.getOpenFileName(self, "Select File")
        else:
            path = qt.QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.lineenc.setText(path)

    def file_dec(self):
        path, _ = qt.QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.linedec.setText(path)
