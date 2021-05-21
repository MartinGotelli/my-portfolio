from datetime import (
    datetime,
)

from django.utils.safestring import SafeString
from googleapiclient.discovery import build

from my_portfolio_web_app.model.financial_instrument import (
    Currency,
    FinancialInstrument,
)
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    Transaction,
    StockDividend,
    CouponClipping,
    Sale,
    Purchase,
)
from services.credentials_manager import CredentialsManager

PRICES_RANGE = 'Cotizaciones Test!A1:B'
OPERATIONS_RANGE = 'Transacciones!A1:Z'


def as_float(string):
    if not string:
        return 0
    else:
        return float(string.replace('U$D', '').replace('$', '').replace('.', '').replace(',', '.'))


class GoogleSheetAPI:
    prices_by_code_cache = {}

    @staticmethod
    def get_credentials():
        return CredentialsManager().google_credentials()

    def get_values_from_sheet(self, range):
        service = build('sheets', 'v4', credentials=self.get_credentials())

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId='1gmEHxkISBwkbGHWfd4M2x-P910kQNy2kajGegIp9kmw',
                                    range=range).execute()

        return result.get('values', [])

    def prices_by_code(self):
        time_now_string = datetime.now().strftime('%Y%d%d%H%M')[:-1]

        if time_now_string in self.prices_by_code_cache:
            return self.prices_by_code_cache[time_now_string]
        else:
            prices_by_code = {}
            for row in self.get_values_from_sheet(PRICES_RANGE):
                # price_string example: $2.000,21
                price_string: str = row[1]
                price = as_float(price_string)
                if price > 0:
                    prices_by_code[row[0]] = price

            self.prices_by_code_cache[time_now_string] = prices_by_code
            return prices_by_code

    def price_for(self, instrument):
        return self.prices_by_code().get(instrument.code, 0)

    def as_operation_data(self, row, header_row):
        return {header: row_value for row_value, header in zip(row, header_row)}

    def operations_from_to(self, from_date, to_date):
        values = self.get_values_from_sheet(OPERATIONS_RANGE)
        header_row = values.pop(0)
        # Si no tiene fecha, lo descarto
        values = (value for value in values if value[1] != '')

        return [GoogleSheetOperationDraft(self.as_operation_data(row, header_row)) for row in values]


OPERATION_CLASSES_BY_TYPE = {
    'C': Purchase,
    'V': Sale,
    'A': CouponClipping,
    'PR': CouponClipping,
    'D': StockDividend,
}


class GoogleSheetOperationDraft:
    def __init__(self, row_data):
        self.number = row_data.get('Num')
        self.type = row_data['Tipo']
        self.financial_instrument_code = row_data['Especie']
        self.quantity = row_data['Nominales'].replace(',', '.')
        self.price_amount = as_float(row_data['Precio $'])
        self.gross_payment = row_data['Bruto $']
        self.date_string = row_data['Fecha']
        self.broker = row_data['Broker']
        self.ars_commissions = as_float(row_data['Total'])
        self.usd_commissions = as_float(row_data['Comisión U$D'])
        self.account_name = row_data['Cuenta']

    def date(self):
        return datetime.strptime(self.date_string, "%d/%m/%Y")

    def currency(self):
        if self.financial_instrument_code.endswith("US$"):
            return Currency.objects.get(code='USD')
        else:
            return Currency.objects.get(code='$')

    def financial_instrument(self):
        # TODO: Qué pasa si el instrumento no existe, hay que crearlo
        return FinancialInstrument.objects.get(code=self.financial_instrument_code)

    def commissions(self):
        # TODO
        return 0

    def price(self):
        return Measurement(self.price_amount, self.currency())

    def account(self):
        return InvestmentIndividualAccount.objects.get(description=self.account_name)

    def operation_class(self):
        return OPERATION_CLASSES_BY_TYPE.get(self.type, Transaction)

    def as_hidden_input(self, value, name):
        return f'<input type ="hidden" name="{name}" value="{value}">'

    def as_hidden(self):
        inputs = [
            self.as_hidden_input(self.date, 'date'),
            self.as_hidden_input(self.quantity, 'security_quantity'),
            self.as_hidden_input(self.financial_instrument().pk, 'financial_instrument'),
            self.as_hidden_input(self.broker, 'broker'),
            self.as_hidden_input(self.ars_commissions, 'ars_commissions'),
            self.as_hidden_input(self.usd_commissions, 'usd_commissions'),
            self.as_hidden_input(self.price().unit.pk, 'price_unit'),
            self.as_hidden_input(self.price().quantity, 'price_amount'),
            self.as_hidden_input(self.account().pk, 'account')
        ]
        return SafeString('\n'.join(inputs))
