from django.test import TestCase
import datetime

from my_portfolio_web_app.model.financial_instrument import Currency, Bond, Stock

today = datetime.date(2020, 2, 2)


class CurrencyTests(TestCase):
    def test_creation(self):
        currency = Currency(code="ARS", description="Pesos")
        self.assertEqual(currency.code, "ARS")
        self.assertEqual(currency.description, "Pesos")

    def test_equals(self):
        ars = Currency(code="ARS", description="Pesos")
        another_ars = Currency(code="ARS", description="Pesos Chilenos")
        self.assertEqual(ars, another_ars)

    def test_is_currency(self):
        self.assertTrue(Currency(code="ARS", description="Pesos").is_currency())

    def test_is_alive(self):
        ars = Currency(code="ARS", description="Pesos")
        self.assertTrue(ars.is_alive_on(today - datetime.timedelta(days=1)))
        self.assertTrue(ars.is_alive_on(today))
        self.assertTrue(ars.is_alive_on(today + datetime.timedelta(days=1)))


class BondTests(TestCase):
    def test_creation(self):
        ay24 = Bond(code="AY24", description="Bonar 2024", maturity_date=today, price_each_quantity=100)
        self.assertEqual(ay24.code, "AY24")
        self.assertEqual(ay24.description, "Bonar 2024")
        self.assertEqual(ay24.maturity_date, today)
        self.assertEqual(ay24.price_each_quantity, 100)

    def test_equals(self):
        ay24 = Bond(code="AY24", description="Bonar 2024", maturity_date=today)
        another_ay24 = Bond(code="AY24", description="Otro bono", maturity_date=today)
        self.assertEqual(ay24, another_ay24)

    def test_is_currency(self):
        self.assertFalse(Bond(code="AY24", description="Bonar 2024", maturity_date=today).is_currency())

    def test_is_alive(self):
        ay24 = Bond(code="AY24", description="Bonar 2024", maturity_date=today)
        self.assertTrue(ay24.is_alive_on(today - datetime.timedelta(days=1)))
        self.assertTrue(ay24.is_alive_on(today))
        self.assertFalse(ay24.is_alive_on(today + datetime.timedelta(days=1)))


class StockTests(TestCase):
    def test_creation(self):
        meli = Stock(code="MELI", description="Mercado Libre")
        self.assertEqual(meli.code, "MELI")
        self.assertEqual(meli.description, "Mercado Libre")

    def test_equals(self):
        meli = Stock(code="MELI", description="Mercado Libre")
        another_meli = Stock(code="MELI", description="Otra acción")
        self.assertEqual(meli, another_meli)

    def test_is_currency(self):
        self.assertFalse(Stock(code="MELI", description="Mercado Libre").is_currency())

    def test_is_alive(self):
        meli = Stock(code="MELI", description="Mercado Libre")
        self.assertTrue(meli.is_alive_on(today - datetime.timedelta(days=1)))
        self.assertTrue(meli.is_alive_on(today))
        self.assertTrue(meli.is_alive_on(today + datetime.timedelta(days=1)))
