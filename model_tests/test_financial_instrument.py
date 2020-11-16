import unittest
import datetime

from model import financial_instrument

today = datetime.date(2020, 2, 2)


class CurrencyTests(unittest.TestCase):
    def test_creation(self):
        currency = financial_instrument.Currency("ARS", "Pesos")
        self.assertEqual(currency.code, "ARS")
        self.assertEqual(currency.description, "Pesos")

    def test_equals(self):
        ars = financial_instrument.Currency("ARS", "Pesos")
        another_ars = financial_instrument.Currency("ARS", "Pesos Chilenos")
        self.assertEqual(ars, another_ars)

    def test_is_currency(self):
        self.assertTrue(financial_instrument.Currency("ARS", "Pesos").is_currency())

    def test_is_alive(self):
        ars = financial_instrument.Currency("ARS", "Pesos")
        self.assertTrue(ars.is_alive_on(today - datetime.timedelta(days=1)))
        self.assertTrue(ars.is_alive_on(today))
        self.assertTrue(ars.is_alive_on(today + datetime.timedelta(days=1)))


class BondTests(unittest.TestCase):
    def test_creation(self):
        ay24 = financial_instrument.Bond("AY24", "Bonar 2024", today)
        self.assertEqual(ay24.code, "AY24")
        self.assertEqual(ay24.description, "Bonar 2024")
        self.assertEqual(ay24.maturity_date, today)

    def test_equals(self):
        ay24 = financial_instrument.Bond("AY24", "Bonar 2024", today)
        another_ay24 = financial_instrument.Bond("AY24", "Otro bono", today)
        self.assertEqual(ay24, another_ay24)

    def test_is_currency(self):
        self.assertFalse(financial_instrument.Bond("AY24", "Bonar 2024", today).is_currency())

    def test_is_alive(self):
        ay24 = financial_instrument.Bond("AY24", "Bonar 2024", today)
        self.assertTrue(ay24.is_alive_on(today - datetime.timedelta(days=1)))
        self.assertTrue(ay24.is_alive_on(today))
        self.assertFalse(ay24.is_alive_on(today + datetime.timedelta(days=1)))


class StockTests(unittest.TestCase):
    def test_creation(self):
        meli = financial_instrument.Stock("MELI", "Mercado Libre")
        self.assertEqual(meli.code, "MELI")
        self.assertEqual(meli.description, "Mercado Libre")

    def test_equals(self):
        meli = financial_instrument.Stock("MELI", "Mercado Libre")
        another_meli = financial_instrument.Stock("MELI", "Otra accion")
        self.assertEqual(meli, another_meli)

    def test_is_currency(self):
        self.assertFalse(financial_instrument.Stock("MELI", "Mercado Libre").is_currency())

    def test_is_alive(self):
        meli = financial_instrument.Stock("MELI", "Mercado Libre")
        self.assertTrue(meli.is_alive_on(today - datetime.timedelta(days=1)))
        self.assertTrue(meli.is_alive_on(today))
        self.assertTrue(meli.is_alive_on(today + datetime.timedelta(days=1)))


if __name__ == '__main__':
    unittest.main()
