import datetime

from environs import Env
from cryptography.fernet import Fernet

env = Env()
env.read_env()

key = env.str('CRIPT_KEY')
cipher_suite = Fernet(key)


def encrypt_data(data):
    if data:
        if isinstance(data, datetime.date):
            data = data.strftime("%Y-%m-%d")
        return cipher_suite.encrypt(data.encode()).decode()
    return data


def decrypt_data(data):
    if not data:
        return data
    decrypted_data = cipher_suite.decrypt(data.encode()).decode()
    try:
        return datetime.datetime.strptime(decrypted_data, "%Y-%m-%d").date()
    except ValueError:
        return decrypted_data
