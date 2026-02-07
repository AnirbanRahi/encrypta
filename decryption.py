import zipfile

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag, InvalidSignature
from cryptography.hazmat.primitives import hmac, hashes



class Decryptor:
    def __init__(self, key_dir, readsize=512 * 1024, iteration=200000):
        self.readsize = readsize
        self.iterations = iteration
        self.key_dir = key_dir
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

    def _find_key_for_magic(self, magic_code_bytes):
        for keyfile in self.key_dir.glob("key*.dat"):
            with open(keyfile, "rb") as f:
                stored_magic = f.read(16)  # 16 bytes
                key_bytes = f.read(32)  # AES key
            if stored_magic == magic_code_bytes:
                return key_bytes
        return None

    def decrypt(self, file: str):

        file = self._fixpath(file)
        p = Path(file)
        filepath = p.parent
        filename = p.stem
        if p.suffix != '.enc':
            raise ValueError(f"{filename} is not encrypted. Try another file.")

        is_dir = filename.endswith(".dir")
        if is_dir:
            filename = filename[:-4]
            newfile = filepath / (filename + ".zip")
        else:
            newfile = filepath / filename

        with open(file, "rb") as finput, open(newfile, "wb") as foutput:
            magic_code = finput.read(16)
            salt = finput.read(16)
            nonce = finput.read(12)
            passkey = finput.read(32)

            keybytes = self._find_key_for_magic(magic_code)
            if keybytes is None:
                raise ValueError("No matching key found for this file's magic code.")

            h = hmac.HMAC(keybytes, hashes.SHA256())
            h.update(salt)
            try:
                h.verify(passkey)
            except InvalidSignature:
                foutput.close()
                os.remove(newfile)
                raise ValueError("Wrong password")
            filesize = os.path.getsize(file)
            encryptedsize = filesize - 16 - 16 - 12 - 16 - 32  # total ciphertext size
            tagposition = filesize - 16
            finput.seek(tagposition)
            tag = finput.read(16)
            cipher = Cipher(algorithms.AES(keybytes), modes.GCM(nonce, tag), backend=self.backend)
            decryptor = cipher.decryptor()

            finput.seek(16 + 16 + 12 + 32)  # skip salt + nonce
            remaining = encryptedsize
            while remaining > 0:
                data = finput.read(min(self.readsize, remaining))
                if not data:
                    break
                originaldata = decryptor.update(data)
                foutput.write(originaldata)
                remaining = remaining - len(data)
            try:
                decryptor.finalize()
            except InvalidTag:
                foutput.close()
                os.remove(newfile)
                raise ValueError("Decryption failed: wrong password or corrupted file")

        if is_dir:
            foldername = filepath / filename
            with zipfile.ZipFile(newfile, "r") as zip_ref:
                zip_ref.extractall(foldername)
            os.remove(newfile)
            os.remove(file)
            return foldername
        else:
            os.remove(file)
            return newfile
