from services.dolar_si_api import DolarSiAPI


class Stock:
    def __init__(self):
        self.code = 'USD'


if __name__ == '__main__':
    print(DolarSiAPI().price_for(Stock()))
