import tkinter as tk
from tkinter import filedialog


def browsefileenc():
    path = filedialog.askopenfilename()
    if path:
        filepathenc.set(path)


def browsefiledec():
    path = filedialog.askopenfilename()
    if path:
        filepathdec.set(path)




window = tk.Tk()
window.title("AES-GCM Encryption Tool")
window.geometry("800x600")

filepathenc = tk.StringVar()
filepathdec = tk.StringVar()

button_enc = tk.Button(window, text="Encrypt")
button_enc.grid(row=0, column=0, padx=10, pady=10)

inputbarenc = tk.Entry(window, textvariable=filepathenc, width=80)
inputbarenc.grid(row=0, column=1, padx=10, pady=10)

browseenc = tk.Button(window, text="Browse", command=browsefileenc)
browseenc.grid(row=0, column=2, padx=10, pady=10)

button_dec = tk.Button(window, text="Decrypt")
button_dec.grid(row=1, column=0, padx=10, pady=10)

inputbardec = tk.Entry(window, textvariable=filepathdec, width=80)
inputbardec.grid(row=1, column=1, padx=10, pady=10)

browsedec = tk.Button(window, text="Browse", command=browsefiledec)
browsedec.grid(row=1, column=2, padx=10, pady=10)

window.mainloop()
