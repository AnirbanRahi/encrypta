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
        self.filepathenc = ""
        self.filepathdec = ""
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

        # Encrypt button
        enc_action_btn = qt.QPushButton("Encrypt")
        enc_action_btn.setFont(font_button)
        enc_action_btn.setStyleSheet(enc_dec_button)
        enc_action_btn.clicked.connect(lambda x: self.encryptfile(self.filepathenc))
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
        dec_action_btn.clicked.connect(lambda x: self.decryptfile(self.filepathdec))
        main_layout.addWidget(dec_action_btn)

        parent.setLayout(main_layout)

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
