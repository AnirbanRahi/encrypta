import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog
from encryption import Encryptor
from decryption import Decryptor


class UI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AES-GCM Encryption Tool")
        self.window.geometry("800x600")

        self.encryptor = Encryptor()
        self.decryptor = Decryptor()
        self.filepathenc = tk.StringVar()
        self.filepathdec = tk.StringVar()

        self.setupui()

    def _browsefileenc(self):
        path = filedialog.askopenfilename()
        if path:
            self.filepathenc.set(path)

    def _browsefiledec(self):
        path = filedialog.askopenfilename()
        if path:
            self.filepathdec.set(path)

    def setupui(self):

        tk.Button(self.window, text="Encrypt", command=self.encryptfile).grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.window, textvariable=self.filepathenc, width=80).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.window, text="Browse", command=self._browsefileenc).grid(row=0, column=2, padx=10, pady=10)

        tk.Button(self.window, text="Decrypt", command=self.decryptfile).grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.window, textvariable=self.filepathdec, width=80).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.window, text="Browse", command=self._browsefiledec).grid(row=1, column=2, padx=10, pady=10)

    def encryptfile(self):
        if not self.filepathenc.get():
            messagebox.showerror("Error", "No file selected for encryption")
            return
        string_path = Path(self.filepathenc.get())
        if string_path.suffix == ".enc":
            messagebox.showerror("Error", "This file is already encrypted!")
            return
        password = simpledialog.askstring("Password", "Enter Password")
        if not password or len(password) < 3:
            messagebox.showerror("Error", "Password must be atlest 3 characters")
            return
        else:
            try:
                newfile = self.encryptor.encrypt(self.filepathenc.get(), password)
                messagebox.showinfo("Success", f"File encrypted: {newfile}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def decryptfile(self):
        if not self.filepathdec.get():
            messagebox.showerror("Error", "No file selected for decryption")
            return
        string_path = Path(self.filepathdec.get())
        if string_path.suffix != ".enc":
            messagebox.showerror("Error", "This file is not encrypted!")
            return
        password = simpledialog.askstring("Password", "Enter Password")
        if not password or len(password) < 3:
            messagebox.showerror("Error", "Password must be atlest 3 characters")
            return
        else:
            try:
                newfile = self.decryptor.decrypt(self.filepathdec.get(), password)
                messagebox.showinfo("Success", f"File encrypted: {newfile}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    ui = UI()
    ui.window.mainloop()
