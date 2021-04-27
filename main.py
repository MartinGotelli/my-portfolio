from services.dolar_si_api import DolarSiAPI

"""if __name__ == '__main__':
    with open('fernet_key.ini', 'r') as key_file:
        fernet_key = bytes(key_file.read(), 'utf-8')

    print(Fernet(fernet_key).encrypt(b'{"user": "mgotelli",'
                               b'"password": "Kilombo6738"}'))
"""


class Stock:
    def __init__(self):
        self.code = 'USD'


if __name__ == '__main__':
    print(DolarSiAPI().price_for(Stock()))
