from datetime import datetime

import requests
from django.contrib.auth.models import User
from django.utils.safestring import SafeString

from my_portfolio_web_app.model.financial_instrument import (
    Currency,
    FinancialInstrument,
    Stock,
)
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    CouponClipping,
    FinancialInstrumentTenderingPayment,
    Purchase,
    Sale,
    StockDividend,
    Transaction,
)
from my_portfolio_web_app.model.user_integration_configuration import UserIntegrationConfiguration

retry = 10


def endpoint(operation):
    return "https://api.invertironline.com/" + operation


class IOLAPI:
    token = None
    token_for_refresh = None
    requests_count = 0
    user = None
    password = None

    def __init__(self, user: User = None):
        self.request_user = user

    def should_retry(self, response):
        if response.status_code == requests.codes.unauthorized:
            self.token_for_refresh = None
            self.refresh_token()
        return response.status_code in [requests.codes.service_unavailable, requests.codes.unauthorized]

    def set_user_and_password(self, request_user):
        try:
            user_configuration = UserIntegrationConfiguration.objects.get(user=request_user)
            self.user = user_configuration.iol_username
            self.password = user_configuration.iol_password
        except UserIntegrationConfiguration.DoesNotExist:
            self.user = ''
            self.password = ''

    def requests(self):
        if not self.user or not self.password:
            self.set_user_and_password(self.request_user)
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
        elif self.should_retry(response) and iteration < retry:
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
        elif self.should_retry(response) and iteration < retry:
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
        elif self.should_retry(response) and iteration < retry:
            return self.operations_from_to(from_date, to_date, iteration + 1)
        else:
            self.error(response)

    def operation_drafts_from(self, json_list):
        operations = []
        payments = []
        commissions_payments = []

        for json in json_list:
            operation_number = json['numero']
            ars_commissions, usd_commissions = self.get_commissions_for(operation_number)
            draft = IOLOperationDraft(operation_number, json['tipo'], json['simbolo'], json['cantidadOperada'],
                                      json['precioOperado'], json['montoOperado'], json['fechaOperada'],
                                      ars_commissions, usd_commissions, self.request_user)
            if draft.is_payment() and not draft.quantity and not draft.gross_payment:
                commissions_payments.append(draft)
            else:
                if draft.is_payment():
                    payments.append(draft)
                operations.append(draft)

        for payment in payments:
            match_payment = next(commissions_payment for commissions_payment in commissions_payments if
                                 self.should_group(payment, commissions_payment))
            payment.group_with(match_payment)
            commissions_payments.remove(match_payment)

        return operations

    @staticmethod
    def should_group(payment, commissions_payment):
        return abs(payment.number - commissions_payment.number) < 5 and \
               payment.date() == commissions_payment.date() and \
               payment.referenced_financial_instrument() == commissions_payment.referenced_financial_instrument() and \
               payment.type == commissions_payment.type

    def get_commissions_for(self, operation_number, iteration=0):
        response = self.requests().get(endpoint(f'api/v2/operaciones/{operation_number}'), headers=self.token_headers())
        if response.status_code == requests.codes.ok:
            return self.find_commissions_in(response.json())
        elif self.should_retry(response) and iteration < retry:
            return self.get_commissions_for(operation_number, iteration + 1)
        else:
            self.error(response)

    @staticmethod
    def find_commissions_in(json):
        ars_commissions = json['arancelesARS']
        usd_commissions = json['arancelesUSD']
        if not ars_commissions and not usd_commissions:
            for commission in json['aranceles']:
                if commission['moneda'] == 'PESO_ARGENTINO':
                    ars_commissions += commission['neto'] + commission['iva']
                else:
                    usd_commissions += commission['neto'] + commission['iva']

        return ars_commissions, usd_commissions


OPERATION_CLASSES_BY_TYPE = {
    'Compra': Purchase,
    'Venta': Sale,
    'Pago de Dividendos': StockDividend,
    'Pago de Renta': CouponClipping,
}


class IOLOperationDraft:
    def __init__(self, number, type, financial_instrument, quantity, price, gross_payment, date, ars_commissions,
                 usd_commissions, user):
        self.number = number
        self.type = type
        self.financial_instrument_code = financial_instrument
        self.quantity = quantity if quantity else 0
        self.price_amount = price if price else 0
        self.gross_payment = gross_payment if gross_payment else 0
        self.date_string = date
        self.ars_commissions = ars_commissions
        self.usd_commissions = usd_commissions
        self.user = user

    def date(self):
        date_str = self.date_string.split('T')[0]
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def security_quantity(self):
        if self.is_payment():
            return self.gross_payment
        else:
            return self.quantity

    def currency(self):
        if self.financial_instrument_code.endswith("US$"):
            return Currency.objects.get(code='USD')
        else:
            return Currency.objects.get(code='$')

    def is_payment(self):
        return issubclass(self.operation_class(), FinancialInstrumentTenderingPayment)

    def financial_instrument(self):
        if self.is_payment():
            return self.currency()
        else:
            return self.real_financial_instrument()

    def real_financial_instrument(self):
        if self.financial_instrument_code.endswith("US$"):
            instrument_code = self.financial_instrument_code.split(" US$")[0]
        else:
            instrument_code = self.financial_instrument_code

        financial_instruments_by_code = FinancialInstrument.objects.filter(code=instrument_code)
        if len(financial_instruments_by_code) == 0:
            Stock.objects.create(code=instrument_code, description=instrument_code)

        return FinancialInstrument.objects.get(code=instrument_code)

    def referenced_financial_instrument_pk(self):
        instrument = self.referenced_financial_instrument()
        if instrument:
            return instrument.pk
        else:
            return instrument

    def referenced_financial_instrument(self):
        if self.is_payment():
            return self.real_financial_instrument()
        else:
            return None

    def price(self):
        return Measurement(self.price_amount, self.currency())

    def operation_class(self):
        return OPERATION_CLASSES_BY_TYPE.get(self.type, Transaction)

    @staticmethod
    def as_hidden_input(value, name):
        return f'<input type ="hidden" name="{name}" value="{value}">'

    def as_hidden(self):
        inputs = [
            self.as_hidden_input(self.date(), 'date'),
            self.as_hidden_input(self.security_quantity(), 'security_quantity'),
            self.as_hidden_input(self.financial_instrument().pk, 'financial_instrument'),
            self.as_hidden_input('IOL', 'broker'),
            self.as_hidden_input(self.ars_commissions, 'ars_commissions'),
            self.as_hidden_input(self.usd_commissions, 'usd_commissions'),
            self.as_hidden_input(self.price().unit.pk, 'price_unit'),
            self.as_hidden_input(self.price().quantity, 'price_amount'),
            self.as_hidden_input(self.referenced_financial_instrument_pk(), 'referenced_financial_instrument')
        ]
        return SafeString('\n'.join(inputs))

    def create(self):
        raise Exception('Todavía no está definido!')
        # kwargs = {
        #     'date': self.date(),
        #     'security_quantity': self.security_quantity(),
        #     'financial_instrument': self.financial_instrument(),
        #     'broker': 'IOL',
        #     'ars_commissions': self.ars_commissions,
        #     'usd_commissions': self.usd_commissions,
        #     'account': InvestmentIndividualAccount.by_user(self.user).first(),
        # }
        # if self.is_payment():
        #     kwargs['referenced_financial_instrument'] = self.referenced_financial_instrument()
        # else:
        #     kwargs['price'] = self.price()

        # self.operation_class().objects.create(**kwargs)

    def group_with(self, commissions_draft):
        self.ars_commissions += commissions_draft.ars_commissions
        self.usd_commissions += commissions_draft.usd_commissions
