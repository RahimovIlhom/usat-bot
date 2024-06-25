import datetime

from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt_data(data):
    if isinstance(data, datetime.date):
        data = data.strftime("%Y-%m-%d")
    return cipher_suite.encrypt(data.encode()).decode()


def decrypt_data(data):
    decrypted_data = cipher_suite.decrypt(data.encode()).decode()
    try:
        return datetime.datetime.strptime(decrypted_data, "%Y-%m-%d").date()
    except ValueError:
        return decrypted_data
