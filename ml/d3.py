from cryptography.fernet import Fernet

encryption_key = b"YfTNC-DjZm__DT4Ss5cLNBc2QXQDOpwLPPGAXzwj0Zc="  # Replace with the key
cipher = Fernet(encryption_key)

with open("clipboard_log.txt", "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()

decrypted_data = cipher.decrypt(encrypted_data)
print(decrypted_data.decode())
