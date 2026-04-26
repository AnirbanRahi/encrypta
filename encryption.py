import shutil

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hmac, hashes


class Encryptor:
    def __init__(self, readsize=512 * 1024, iteration=200000):
        self.readsize = readsize
        self.iterations = iteration
        self.backend = default_backend()


    def _fixpath(self, filepath):
        if not filepath:
            raise ValueError("Empty file path")
        if filepath[0] == "\"" or filepath[0] == "\'":
            filepath = filepath[1:]
        if filepath[-1] == "\"" or filepath[-1] == "\'":
            filepath = filepath[:-1]
        filepath = filepath.replace("\\", "/")
        filepath = filepath.replace("\\\\", "/")
        return filepath

    def encrypt(self, file: str, password: str):

        file = self._fixpath(file)
        p = Path(file)
        filepath = p.parent
        filename = p.stem
        fileextension = p.suffix
        if p.suffix == '.enc':
            raise ValueError("File is already encrypted")

        if p.is_dir():
            zipname = str(p)
            shutil.make_archive(zipname, "zip", p)
            readfile = zipname + ".zip"
            newfile = Path(zipname + ".dir" + ".enc")
        else:
            readfile = file
            newfile = filepath / (filename + fileextension + ".enc")


        nonce = os.urandom(12)
        salt = os.urandom(16)
        password = password.encode('utf-8')

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        keybytes = kdf.derive(password)

        verifier = hashes.Hash(hashes.SHA256(), backend=self.backend)
        verifier.update(keybytes)
        verifier = verifier.finalize()[:16]

        cipher = Cipher(algorithms.AES(keybytes), modes.GCM(nonce), backend=self.backend)
        encryptor = cipher.encryptor()

        with open(readfile, "rb") as finput, open(newfile, "wb") as foutput:
            foutput.write(salt)
            foutput.write(nonce)
            foutput.write(verifier)

            while True:
                data = finput.read(self.readsize)  # try to read upto readsize and return it
                if not data:
                    break
                ciphertext = encryptor.update(data)
                foutput.write(ciphertext)

            foutput.write(encryptor.finalize())
            foutput.write(encryptor.tag)
        if p.is_dir():
            shutil.rmtree(p)
            os.remove(readfile)
        else:
            os.remove(file)
        return newfile
