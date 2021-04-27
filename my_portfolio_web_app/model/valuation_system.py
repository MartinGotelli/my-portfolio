import datetime

from my_portfolio_web_app.model.exceptions import ObjectNotFound
from my_portfolio_web_app.model.financial_instrument import Currency
from my_portfolio_web_app.model.measurement import Measurement
from services.dolar_si_api import DolarSiAPI
from services.google_sheet_api import GoogleSheetAPI
from services.iol_api import IOLAPI


class ValuationSourceFromDictionary:
    def __init__(self, prices=None):
        if prices is None:
            prices = {}
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
        if instrument == currency:
            return Measurement(1, currency)

        try:
            return next(filter(lambda price: price.unit == currency,
                               self.prices_for_on(instrument, date)))
        except StopIteration:
            raise ObjectNotFound(
                "There is no " + currency.description + " price for " + instrument.code + " on " + str(date))


class ValuationSourceFromIOLAPI:
    source = ValuationSourceFromDictionary()

    def __init__(self, instruments_api=IOLAPI(), currencies_api=DolarSiAPI()):
        self.instruments_api = instruments_api
        self.currencies_api = currencies_api

    def api_for(self, instrument):
        if instrument.is_currency():
            return self.currencies_api
        else:
            return self.instruments_api

    def price_for_on(self, instrument, currency, date):
        if instrument == currency:
            return Measurement(1, instrument)
        else:
            if not instrument.is_alive_on(date):
                return Measurement(0, currency)
            else:
                try:
                    price = self.source.price_for_on(instrument, currency, date)
                    return price
                except ObjectNotFound:
                    if date == datetime.date.today():
                        try:
                            price = Measurement(self.api_for(instrument).price_for(instrument), currency)
                            self.source.add_price_for_on(instrument, date, price)
                            return price
                        except Exception as exception:
                            # TODO: Hacer bien
                            print(exception)
                            return Measurement(0, currency)
                    else:
                        raise ObjectNotFound(
                            "There is no " + currency.description + "price for " + instrument.code + " on " + str(date))


class CurrenciesValuationSource:
    source = ValuationSourceFromDictionary()

    def price_for_on(self, instrument, currency, date):
        if not instrument.is_currency():
            return Measurement(0, currency)

        if instrument == currency:
            return Measurement(1, instrument)
        else:
            try:
                return self.source.price_for_on(instrument, currency, date)
            except ObjectNotFound:
                if date == datetime.date.today():
                    try:
                        price = Measurement(DolarSiAPI().price_for(currency), currency)
                        self.source.add_price_for_on(instrument, date, price)
                        return price
                    except Exception as exception:
                        # TODO: Hacer bien
                        print(exception)
                        return Measurement(0, currency)
                else:
                    raise ObjectNotFound(
                        "There is no " + currency.description + "price for " + instrument.code + " on " + str(date))


class ValuationSourceFromGoogleSheet:
    source = ValuationSourceFromDictionary()

    def price_for_on(self, instrument, currency, date):
        try:
            price = self.source.price_for_on(instrument, currency, date)
            return price
        except ObjectNotFound:
            price = Measurement(GoogleSheetAPI().price_for(instrument), currency)
            self.source.add_price_for_on(instrument, date, price)
            return price


class ValuationByBruteForce:
    def __init__(self, strategies):
        self.strategies = strategies

    def price_for_on(self, instrument, currency, date):
        if not instrument.is_alive_on(date):
            return Measurement(0, currency)
        else:
            for valuation_strategy in self.strategies:
                price = valuation_strategy.price_for_on(instrument, currency, date)
                if price != 0:
                    return price
            return Measurement(0, currency)


class ValuationSystem:
    def __init__(self, source):
        self.source = source

    def valuate_account_on(self, account, currency, date, broker=None):
        return sum(
            [self.valuate_instrument_on(balance.unit, currency, date) * float(balance) for balance in
             account.balances_on(date, broker).as_bag().measurements])

    def valuate_transaction_on(self, transaction, currency, date):
        return float(transaction.security_quantity_if_alive_on(date)) * self.valuate_instrument_on(
            transaction.financial_instrument, currency, date)

    def valuate_instrument_on(self, instrument, currency, date):
        # TODO: Siempre valúo pesos
        return Measurement(float(self.source.price_for_on(instrument, currency, date)), Currency.objects.get(code='$'))
