from datetime import datetime

import requests

from my_portfolio_web_app.model.financial_instrument import (
    Currency,
    FinancialInstrument,
)
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    StockDividend,
    Purchase,
    Sale,
    Transaction,
)
from services.credentials_manager import CredentialsManager

retry = 10


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def endpoint(operation):
    return "https://api.invertironline.com/" + operation


class IOLAPI(metaclass=Singleton):
    token = None
    token_for_refresh = None
    requests_count = 0
    user = None
    password = None

    def __init__(self):
        self.set_user_and_password()

    def set_user_and_password(self):
        credentials_manager = CredentialsManager()
        self.user = credentials_manager.iol_username()
        self.password = credentials_manager.iol_password()

    def requests(self):
        self.requests_count += 1
        return requests

    def get_token(self):
        if self.token is None:
            self.refresh_token()
        return self.token

    def error(self, response, financial_instrument=""):
        raise Exception(response.reason + " " + financial_instrument)

    def refresh_token(self, iteration=0):
        if self.token_for_refresh is None:
            response = self.requests().get(endpoint("token"),
                                           data={
                                               "username": self.user, "password": self.password,
                                               "grant_type": "password"})
        else:
            response = self.requests().get(endpoint("token"), data={
                "refresh_token": self.token_for_refresh,
                "grant_type": "refresh_token"})
        if response.status_code == requests.codes.ok:
            self.token = response.json()["access_token"]
            self.token_for_refresh = response.json()["refresh_token"]
        elif response.status_code == requests.codes.service_unavailable and iteration < retry:
            self.refresh_token(iteration + 1)
        else:
            self.error(response)

    def token_headers(self):
        return {"Authorization": "Bearer " + self.get_token()}

    def price_for(self, financial_instrument, iteration=0):
        response = self.requests().get(endpoint("api/v2/bCBA/Titulos/" + financial_instrument.code + "/Cotizacion"),
                                       data={"simbolo": financial_instrument.code, "mercado": "bCBA", "plazo": "t2"},
                                       headers=self.token_headers())
        if response.status_code == requests.codes.ok:
            return float(response.json()["ultimoPrecio"]) / financial_instrument.price_each_quantity
        elif response.status_code == requests.codes.service_unavailable and iteration < retry:
            return self.price_for(financial_instrument, iteration + 1)
        else:
            self.error(response, financial_instrument.code)

    def operations_from_to(self, from_date, to_date, iteration=0):
        response = self.requests().get(endpoint('api/v2/operaciones'),
                                       params={
                                           'filtro.estado': 'terminadas', 'filtro.fechaDesde': from_date,
                                           'filtro.fechaHasta': to_date}, headers=self.token_headers())
        if response.status_code == requests.codes.ok:
            return self.operation_drafts_from(response.json())
        elif response.status_code == requests.codes.service_unavailable and iteration < retry:
            return self.operations_from_to(from_date, to_date, iteration + 1)
        elif response.status_code == requests.codes.unauthorized:
            self.token_for_refresh = None
            self.refresh_token()
            return self.operations_from_to(from_date, to_date, iteration)
        else:
            self.error(response)

    def operation_drafts_from(self, json_list):
        return [IOLOperationDraft(json["numero"], json["tipo"], json["simbolo"], json["cantidadOperada"],
                                  json["precioOperado"], json["montoOperado"], json["fechaOperada"]) for json in
                json_list]


OPERATION_CLASSES_BY_TYPE = {
    'Compra': Purchase,
    'Venta': Sale,
    'Pago de Dividendos': StockDividend,
}


class IOLOperationDraft:
    def __init__(self, number, type, financial_instrument, quantity, price, gross_payment, date):
        self.number = number
        self.type = type
        self.financial_instrument_code = financial_instrument
        self.quantity = quantity
        self.price_amount = price
        self.gross_payment = gross_payment
        self.date_string = date

    def date(self):
        return datetime.strptime(self.date_string, "%Y-%m-%dT%H:%M:%S").date()

    def currency(self):
        if self.financial_instrument_code.endswith("US$"):
            return Currency.objects.get(code='USD')
        else:
            return Currency.objects.get(code='$')

    def financial_instrument(self):
        if self.financial_instrument_code.endswith("US$"):
            instrument_code = self.financial_instrument_code.split(" US$")[0]
        else:
            instrument_code = self.financial_instrument_code

        # TODO: Qué pasa si el instrumento no existe, hay que crearlo
        return FinancialInstrument.objects.get(code=instrument_code)

    def commissions(self):
        # TODO, hay que buscar la operación por número y sumar los aranceles
        return 0

    def price(self):
        return Measurement(self.price_amount, self.currency())

    def operation_class(self):
        return OPERATION_CLASSES_BY_TYPE.get(self.type, Transaction)
