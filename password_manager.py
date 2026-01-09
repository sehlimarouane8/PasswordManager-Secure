from cryptography.fernet import Fernet
import os

KEY_FILE = "key.key"
DATA_FILE = "passwords.enc"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

def encrypt_data(data):
    f = Fernet(load_key())
    return f.encrypt(data.encode())

def decrypt_data(data):
    f = Fernet(load_key())
    return f.decrypt(data).decode()

def add_password(service, password):
    entry = f"{service}:{password}\n"
    encrypted = encrypt_data(entry)

    with open(DATA_FILE, "ab") as f:
        f.write(encrypted + b"\n")

def read_passwords():
    if not os.path.exists(DATA_FILE):
        print("No stored passwords.")
        return

    with open(DATA_FILE, "rb") as f:
        for line in f:
            try:
                print(decrypt_data(line.strip()))
            except:
                pass

if __name__ == "__main__":
    if not os.path.exists(KEY_FILE):
        generate_key()

    choice = input("1- Add password\n2- View passwords\nChoose: ")

    if choice == "1":
        s = input("Service: ")
        p = input("Password: ")
        add_password(s, p)
        print("Password stored securely.")
    elif choice == "2":
        read_passwords()
