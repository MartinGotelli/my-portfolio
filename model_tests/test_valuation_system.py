import unittest
from datetime import date

from model.exceptions import ObjectNotFound
from model.financial_instrument import Currency, Bond, Stock
from model.investment_account import InvestmentAccount, InvestmentIndividualAccount
from model.measurement import Measurement
from model.transaction import Purchase, Sale
from model.valuation_system import ValuationSourceFromDictionary, ValuationSystem

ars = Currency('$', 'Pesos')
usd = Currency('U$D', 'Dólares')
one_peso = Measurement(1, ars)
today = date(2020, 2, 2)
tomorrow = date(2020, 2, 3)
after_tomorrow = date(2020, 2, 4)
ay24 = Bond('AY24', 'Bonar 2024', tomorrow)
meli = Stock("MELI", "MERCADOLIBRE")


def ars_for(amount):
    return Measurement(amount, ars)


def usd_for(amount):
    return Measurement(amount, usd)


valuation_source = ValuationSourceFromDictionary({
    today: {
        ay24: [ars_for(200), usd_for(1.23)],
        meli: [ars_for(1150)]
    },
    tomorrow: {
        ay24: [ars_for(210), usd_for(1.23)]
    }
})

valuation_system = ValuationSystem(valuation_source)


class TestValuationFromDictionary(unittest.TestCase):
    def test_creation(self):
        mock_valuation_source = ValuationSourceFromDictionary({})
        mock_valuation_source.prices = {}

    def test_add_price(self):
        source = ValuationSourceFromDictionary({})
        with self.assertRaises(ObjectNotFound):
            source.price_for_on(meli, usd, today)
        source.add_price_for_on(meli, today, usd_for(10))
        self.assertEqual(source.price_for_on(meli, usd, today), usd_for(10))

    def test_add_price_replacing_previous_price(self):
        source = ValuationSourceFromDictionary({})
        with self.assertRaises(ObjectNotFound):
            source.price_for_on(meli, usd, today)
        source.add_price_for_on(meli, today, usd_for(10))
        self.assertEqual(source.price_for_on(meli, usd, today), usd_for(10))
        source.add_price_for_on(meli, today, usd_for(10.5))
        self.assertEqual(source.price_for_on(meli, usd, today), usd_for(10.5))

    def test_price_of_on(self):
        self.assertEqual(valuation_source.price_for_on(ay24, ars, today), ars_for(200))
        self.assertEqual(valuation_source.price_for_on(ay24, usd, today), usd_for(1.23))
        self.assertEqual(valuation_source.price_for_on(meli, ars, today), ars_for(1150))
        self.assertEqual(valuation_source.price_for_on(ay24, ars, tomorrow), ars_for(210))

    def test_price_for_non_existent_currency(self):
        with self.assertRaises(ObjectNotFound):
            valuation_source.price_for_on(meli, usd, today)

    def test_price_for_non_existent_instrument(self):
        with self.assertRaises(ObjectNotFound):
            valuation_source.price_for_on(ars, ars, today)
        with self.assertRaises(ObjectNotFound):
            valuation_source.price_for_on(meli, ars, tomorrow)

    def test_price_for_non_existent_date(self):
        with self.assertRaises(ObjectNotFound):
            valuation_source.price_for_on(ay24, ars, after_tomorrow)


class TestValuationSystem(unittest.TestCase):
    def test_creation(self):
        mock_valuation_system = ValuationSystem("source")
        self.assertEqual(mock_valuation_system.source, "source")

    def test_valuate_instrument_on(self):
        self.assertEqual(valuation_system.valuate_instrument_on(ay24, ars, today), ars_for(200))

    def test_valuate_transaction_on(self):
        purchase = Purchase(today, 2000, ay24, ars_for(180), "IOL")
        self.assertEqual(valuation_system.valuate_transaction_on(purchase, ars, today), ars_for(200 * 2000))

    def test_valuate_account_on(self):
        purchase = Purchase(today, 2000, ay24, ars_for(180), "IOL")
        another_purchase = Purchase(today, 100, ay24, ars_for(185), "IOL")
        sale = Sale(today, 1200, ay24, ars_for(205), "IOL")
        account = InvestmentIndividualAccount("Martín")
        account.add_transaction(purchase)
        account.add_transaction(another_purchase)
        account.add_transaction(sale)
        self.assertEqual(valuation_system.valuate_account_on(account, ars, today), ars_for(200 * (2000 + 100 - 1200)))
