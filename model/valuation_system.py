import datetime

from model.exceptions import ObjectNotFound
from model.measurement import Measurement
from services.dolar_si_api import DolarSiAPI
from services.iol_api import IOLAPI


class ValuationSourceFromDictionary:
    def __init__(self, prices={}):
        self.prices = prices

    def prices_for_on(self, instrument, date):
        return self.prices.setdefault(date, {}).setdefault(instrument, [])

    def add_price_for_on(self, instrument, date, price):
        self.remove_if_exist_price_for_on(instrument, date, price.unit)
        self.prices_for_on(instrument, date).append(price)

    def remove_if_exist_price_for_on(self, instrument, date, currency):
        try:
            price_to_remove = self.price_for_on(instrument, currency, date)
            self.prices_for_on(instrument, date).remove(price_to_remove)
        except ObjectNotFound:
            pass

    def price_for_on(self, instrument, currency, date):
        try:
            return next(filter(lambda price: price.unit == currency,
                               self.prices_for_on(instrument, date)))
        except StopIteration:
            raise ObjectNotFound(
                "There is no " + currency.description + "price for " + instrument.code + " on " + str(date))


class ValuationSourceFromIOLAPI:
    def __init__(self, instruments_api=IOLAPI(), currencies_api=DolarSiAPI(), source=ValuationSourceFromDictionary()):
        self.instruments_api = instruments_api
        self.currencies_api = currencies_api
        self.source = source

    def api_for(self, instrument):
        if instrument.is_currency():
            return self.currencies_api
        else:
            return self.instruments_api

    def price_for_on(self, instrument, currency, date):
        #TODO: if instrument == currency:
        if instrument.is_currency():
            return Measurement(1, instrument)
        else:
            try:
                return self.source.price_for_on(instrument, currency, date)
            except ObjectNotFound:
                if date == datetime.date.today():
                    try:
                        price = Measurement(self.api_for(instrument).price_for(instrument), currency)
                        self.source.add_price_for_on(instrument, date, price)
                        return price
                    except Exception as exception:
                        # TODO: Hacer bien
                        print(exception)
                        return 0
                else:
                    raise ObjectNotFound(
                        "There is no " + currency.description + "price for " + instrument.code + " on " + str(date))


class ValuationSystem:
    def __init__(self, source):
        self.source = source

    def valuate_account_on(self, account, currency, date, broker="None"):
        return sum(
            [self.valuate_instrument_on(balance.unit, currency, date) * float(balance) for balance in
             account.balances_on(date, broker).measurements])

    def valuate_transaction_on(self, transaction, currency, date):
        return float(transaction.security_quantity_if_alive_on(date)) * self.valuate_instrument_on(
            transaction.financial_instrument, currency, date)

    def valuate_instrument_on(self, instrument, currency, date):
        return self.source.price_for_on(instrument, currency, date)
