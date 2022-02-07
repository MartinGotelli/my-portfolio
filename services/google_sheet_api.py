from datetime import (
    datetime,
)

from django.utils.safestring import SafeString
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from my_portfolio_web_app.model.financial_instrument import (
    Currency,
    FinancialInstrument,
    Stock,
)
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.transaction import (
    CouponClipping,
    FinancialInstrumentTenderingPayment,
    Inflow,
    Outflow,
    Purchase,
    Sale,
    StockDividend,
    Transaction,
)
from my_portfolio_web_app.model.user_integration_configuration import UserIntegrationConfiguration

PRICES_RANGE = 'Cotizaciones!A1:B'
OPERATIONS_RANGE = 'Transacciones!A1:Z'
CASH_FLOWS_RANGE = 'Depositos!A1:H'


# SHEET_ID = '1oaDgLdxTyQJN6k-gcNNBBF7T-qyTQY6fZ1f09d0e7AI'  # Michu
# SHEET_ID = '1gmEHxkISBwkbGHWfd4M2x-P910kQNy2kajGegIp9kmw'  # Martín


def as_float(string):
    if not string:
        return 0
    else:
        if '-' in string:
            sign = -1
        else:
            sign = 1
        return sign * float(
            string.replace('-', '').replace('U$D', '').replace('$', '').replace('.', '').replace(',', '.'))


class GoogleSheetAPI:
    prices_by_code_cache = {}

    def __init__(self, request):
        self.user = request.user
        self.sheet_id = UserIntegrationConfiguration.objects.get(user=self.user).google_sheet_id
        self.credentials = Credentials.from_authorized_user_info(request.session.get('google_credentials'))

    def get_values_from_sheet(self, range):
        service = build('sheets', 'v4', credentials=self.credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id,
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

    @staticmethod
    def as_operation_data(row, header_row):
        return {header: row_value for row_value, header in zip(row, header_row)}

    def transactions_from_to(self, sheet_range, draft_class, from_date_string, to_date_string, without_filter=False):
        values = self.get_values_from_sheet(sheet_range)
        header_row = values.pop(0)
        date_index = header_row.index('Fecha')
        # Si no tiene fecha, lo descarto
        values = (value for value in values if len(value) > date_index and value[date_index] != '')

        drafts = []
        from_date = without_filter or datetime.strptime(from_date_string, '%Y-%m-%d').date()
        to_date = without_filter or datetime.strptime(to_date_string, '%Y-%m-%d').date()

        for row in values:
            date = datetime.strptime(row[date_index], '%d/%m/%Y').date()
            if without_filter or from_date <= date <= to_date:
                drafts.append(draft_class(self.as_operation_data(row, header_row), self.user))

        return drafts

    def operations_from_to(self, from_date_string, to_date_string, without_filter=False):
        return self.transactions_from_to(OPERATIONS_RANGE, GoogleSheetOperationDraft, from_date_string, to_date_string,
                                         without_filter)

    def cash_flows_from_to(self, from_date_string, to_date_string, without_filter=False):
        return self.transactions_from_to(CASH_FLOWS_RANGE, GoogleSheetCashFlowDraft, from_date_string, to_date_string,
                                         without_filter)


OPERATION_CLASSES_BY_TYPE = {
    'C': Purchase,
    'V': Sale,
    'A': CouponClipping,
    'PR': CouponClipping,
    'D': StockDividend,
    'I': Inflow,
    'E': Outflow,
}


class GoogleSheetOperationDraft:
    def __init__(self, row_data, user):
        self.number = row_data.get('Num') or 0
        self.type = row_data['Tipo']
        self.financial_instrument_code = row_data['Especie']
        self.currency_code = row_data['Moneda']
        self.quantity = abs(as_float(row_data['Nominales']))
        self.ars_price_amount = as_float(row_data['Precio $'])
        self.ars_gross_payment_string = row_data['Bruto $']
        self.ars_gross_payment = as_float(self.ars_gross_payment_string)
        self.usd_price_amount = as_float(row_data['Precio U$D'])
        self.usd_gross_payment_string = row_data['Bruto U$D']
        self.usd_gross_payment = as_float(self.usd_gross_payment_string)
        self.date_string = row_data['Fecha']
        self.broker = row_data['Broker']
        self.ars_commissions = round(as_float(row_data['Comisión']) + as_float(row_data['Derechos']), 2)
        self.usd_commissions = round(as_float(row_data['Comisión U$D']), 2)
        self.account_name = row_data['Cuenta']
        self.user = user

    def create(self):
        kwargs = {
            'date': self.date(),
            'security_quantity': self.security_quantity(),
            'financial_instrument': self.financial_instrument(),
            'broker': self.broker,
            'ars_commissions': self.ars_commissions,
            'usd_commissions': self.usd_commissions,
            'account': self.account(),
        }
        if self.is_payment():
            kwargs['referenced_financial_instrument'] = self.referenced_financial_instrument()
        else:
            kwargs['price'] = self.price()

        self.operation_class().objects.create(**kwargs)

    def date(self):
        return datetime.strptime(self.date_string, "%d/%m/%Y").date()

    def security_quantity(self):
        if self.is_payment():
            if self.currency() == self.ars():
                return self.ars_gross_payment
            else:
                return self.usd_gross_payment
        else:
            return self.quantity

    @staticmethod
    def ars():
        currencies = Currency.objects.filter(code='$')
        if not currencies:
            return Currency.objects.create(code='$', description='Pesos')
        return Currency.objects.get(code='$')

    @staticmethod
    def usd():
        currencies = Currency.objects.filter(code='USD')
        if not currencies:
            Currency.objects.create(code='USD', description='Dólares')
        return Currency.objects.get(code='USD')

    def is_payment(self):
        return issubclass(self.operation_class(), FinancialInstrumentTenderingPayment)

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

    def currency(self):
        if not self.currency_code:
            if self.ars_gross_payment:
                return self.ars()
            else:
                return self.usd()
        else:
            return Currency.objects.get(code=self.currency_code)

    def financial_instrument(self):
        if self.is_payment():
            return self.currency()
        else:
            return self.real_financial_instrument()

    def real_financial_instrument(self):
        financial_instruments_by_code = FinancialInstrument.objects.filter(code=self.financial_instrument_code)
        if len(financial_instruments_by_code) == 0:
            Stock.objects.create(code=self.financial_instrument_code,
                                 description=self.financial_instrument_code)

        return FinancialInstrument.objects.get(code=self.financial_instrument_code)

    def price(self):
        if self.currency() == self.ars():
            return Measurement(self.ars_price_amount, self.currency())
        else:
            return Measurement(self.usd_price_amount, self.currency())

    def account(self):
        return get_or_create_account(self.account_name, self.user)

    def operation_class(self):
        return OPERATION_CLASSES_BY_TYPE.get(self.type, Transaction)

    def as_hidden_input(self, value, name):
        return f'<input type ="hidden" name="{name}" value="{value}">'

    def as_hidden(self):
        inputs = [
            self.as_hidden_input(self.date(), 'date'),
            self.as_hidden_input(self.security_quantity(), 'security_quantity'),
            self.as_hidden_input(self.financial_instrument().pk, 'financial_instrument'),
            self.as_hidden_input(self.broker, 'broker'),
            self.as_hidden_input(self.ars_commissions, 'ars_commissions'),
            self.as_hidden_input(self.usd_commissions, 'usd_commissions'),
            self.as_hidden_input(self.price().unit.pk, 'price_unit'),
            self.as_hidden_input(self.price().quantity, 'price_amount'),
            self.as_hidden_input(self.account().pk, 'account'),
            self.as_hidden_input(self.referenced_financial_instrument_pk(), 'referenced_financial_instrument')
        ]
        return SafeString('\n'.join(inputs))


class GoogleSheetCashFlowDraft:
    def __init__(self, row_data, user):
        self.number = row_data.get('Num') or 0
        self.date_string = row_data['Fecha']
        self.type = row_data['Tipo']
        self.broker = row_data['Broker']
        self.account_name = row_data['Cuenta']
        self.financial_instrument_code = row_data['Moneda']
        self.quantity = abs(as_float(row_data['Nominales']))
        self.user = user

    def create(self):
        kwargs = {
            'date': self.date(),
            'security_quantity': self.security_quantity(),
            'financial_instrument': self.financial_instrument(),
            'broker': self.broker,
            'account': self.account(),
        }
        self.operation_class().objects.create(**kwargs)

    def date(self):
        return datetime.strptime(self.date_string, "%d/%m/%Y").date()

    def security_quantity(self):
        return self.quantity

    @staticmethod
    def ars():
        return Currency.objects.get(code='$')

    @staticmethod
    def usd():
        return Currency.objects.get(code='USD')

    def is_payment(self):
        return issubclass(self.operation_class(), FinancialInstrumentTenderingPayment)

    def financial_instrument(self):
        return self.real_financial_instrument()

    def real_financial_instrument(self):
        financial_instruments_by_code = FinancialInstrument.objects.filter(code=self.financial_instrument_code)
        if len(financial_instruments_by_code) == 0:
            Currency.objects.create(code=self.financial_instrument_code, description=self.financial_instrument_code)

        return FinancialInstrument.objects.get(code=self.financial_instrument_code)

    def account(self):
        return get_or_create_account(self.account_name, self.user)

    def operation_class(self):
        return OPERATION_CLASSES_BY_TYPE.get(self.type, Transaction)

    def as_hidden_input(self, value, name):
        return f'<input type ="hidden" name="{name}" value="{value}">'

    def as_hidden(self):
        inputs = [
            self.as_hidden_input(self.date(), 'date'),
            self.as_hidden_input(self.security_quantity(), 'security_quantity'),
            self.as_hidden_input(self.financial_instrument().pk, 'financial_instrument'),
            self.as_hidden_input(self.broker, 'broker'),
            self.as_hidden_input(self.account().pk, 'account'),
        ]
        return SafeString('\n'.join(inputs))


def get_or_create_account(account_name, user):
    accounts_by_name = InvestmentIndividualAccount.objects.filter(description=account_name)
    if accounts_by_name:
        return accounts_by_name[0]
    else:
        account = InvestmentIndividualAccount.objects.create(description=account_name)
        account.authorized_users.add(user)
        return account