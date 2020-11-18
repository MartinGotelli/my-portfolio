import requests

from services.iol_api import Singleton


class DolarSiAPI(metaclass=Singleton):

    def error(self, response):
        raise Exception(response.reason + " - USD")

    def price_for(self, instrument):
        endpoint = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        response = requests.get(endpoint)
        if response.status_code == requests.codes.ok:
            return next([float(dollarJson["casa"]["venta"]) for dollarJson in response.json() if
                         dollarJson["casa"]["nombre"] == "Dolar Bolsa"])
        else:
            self.error(response)
