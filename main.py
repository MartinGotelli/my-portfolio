import json
import os
from getpass import getpass

from cryptography.fernet import Fernet

from services.credentials_manager import IOL_INI


def create_IOL_credentials(username, password):
    if not os.path.exists('fernet_key.ini'):
        with open('fernet_key.ini', 'w') as key_file:
            key_file.write(Fernet.generate_key().decode('utf-8'))

    with open('fernet_key.ini', 'r') as key_file:
        fernet_key = bytes(key_file.read(), 'utf-8')

    user_and_password_json = json.dumps({
        'user': username,
        'password': password
    })

    encrypted_data = Fernet(fernet_key).encrypt(bytes(user_and_password_json, 'utf-8'))

    with open(IOL_INI, 'w') as iol_ini:
        iol_ini.write(encrypted_data.decode('utf-8'))

    print('Archivo creado')


if __name__ == '__main__':
    user = input('Insert IOL username:\n')
    password = getpass('Insert IOL password:\n')
    create_IOL_credentials(user, password)
