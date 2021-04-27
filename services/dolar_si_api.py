import requests

from my_portfolio_web_app.model.financial_instrument import Currency


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DolarSiAPI(metaclass=Singleton):

    def error(self, response):
        raise Exception(response.reason + " - USD")

    def price_for(self, instrument):
        endpoint = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        response = requests.get(endpoint)
        if response.status_code == requests.codes.ok:
            dollar_price_json = next((dollar_json for dollar_json in response.json() if
                                      dollar_json["casa"]["nombre"] == "Dolar Bolsa"))
            dollar_string = dollar_price_json["casa"]["venta"]

            dollar_price = float(dollar_string.replace(',', '.'))

            if instrument == Currency.objects.get(code='$'):
                return dollar_price
            else:
                return 1 / dollar_price

        else:
            self.error(response)
