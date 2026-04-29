import PyQt6.QtWidgets as qt
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap
from styles import *
from PyQt6.QtWidgets import QStackedWidget, QLineEdit


class Mainpage(qt.QWidget):
    def mainpage(self, encryptfile, decryptfile, parent: qt.QWidget, stack=QStackedWidget):
        self.parent = parent
        self.stack = stack
        self.encryptfile = encryptfile
        self.decryptfile = decryptfile

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
        self.enc_mode = "file"
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

        # Encryption Password
        enc_pass_layout = qt.QHBoxLayout()
        self.enc_password = qt.QLineEdit()
        self.enc_password.setPlaceholderText("Enter encryption password")
        self.enc_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.enc_password.setStyleSheet(line_style)
        self.enc_password.setClearButtonEnabled(True)
        self.enc_toggle_btn = qt.QPushButton("Show")
        self.enc_toggle_btn.setCheckable(True)
        self.enc_toggle_btn.setStyleSheet(inactive_button)
        self.enc_toggle_btn.clicked.connect(self.toggle_enc_password)
        enc_pass_layout.addWidget(self.enc_password)
        enc_pass_layout.addWidget(self.enc_toggle_btn)
        main_layout.addLayout(enc_pass_layout)

        # Encrypt button
        enc_action_btn = qt.QPushButton("Encrypt")
        enc_action_btn.setFont(font_button)
        enc_action_btn.setStyleSheet(enc_dec_button)
        enc_action_btn.clicked.connect(
            lambda _: self.handle_encrypt()
        )
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

        # Decryption Password
        dec_pass_layout = qt.QHBoxLayout()
        self.dec_password = qt.QLineEdit()
        self.dec_password.setPlaceholderText("Enter decryption password")
        self.dec_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.dec_password.setStyleSheet(line_style)
        self.dec_password.setClearButtonEnabled(True)
        self.dec_toggle_btn = qt.QPushButton("Show")
        self.dec_toggle_btn.setCheckable(True)
        self.dec_toggle_btn.setStyleSheet(inactive_button)
        self.dec_toggle_btn.clicked.connect(self.toggle_dec_password)
        dec_pass_layout.addWidget(self.dec_password)
        dec_pass_layout.addWidget(self.dec_toggle_btn)
        main_layout.addLayout(dec_pass_layout)

        # Decrypt button
        dec_action_btn = qt.QPushButton("Decrypt")
        dec_action_btn.setStyleSheet(enc_dec_button)
        dec_action_btn.setFont(font_button)
        dec_action_btn.clicked.connect(
            lambda _: self.handle_decrypt()
        )
        main_layout.addWidget(dec_action_btn)

        parent.setLayout(main_layout)

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
            self.enc_toggle_btn.setText("Show")
            self.enc_password.setEchoMode(QLineEdit.EchoMode.Password)

    def handle_decrypt(self):
        success = self.decryptfile(self.linedec.text(), self.dec_password.text())

        if success:
            self.linedec.clear()
            self.dec_password.clear()

            self.dec_toggle_btn.setChecked(False)
            self.dec_toggle_btn.setText("Show")
            self.dec_password.setEchoMode(QLineEdit.EchoMode.Password)

    def toggle_enc_password(self):
        if self.enc_toggle_btn.isChecked():
            self.enc_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.enc_toggle_btn.setText("Hide")
        else:
            self.enc_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.enc_toggle_btn.setText("Show")

    def toggle_dec_password(self):
        if self.dec_toggle_btn.isChecked():
            self.dec_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.dec_toggle_btn.setText("Hide")
        else:
            self.dec_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.dec_toggle_btn.setText("Show")

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
