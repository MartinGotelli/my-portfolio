import unittest
from model import financial_instrument, transaction
import datetime

euro = financial_instrument.Currency('EUR', 'Euro')
today = datetime.date(2020, 2, 2)
ay24 = financial_instrument.Currency('AY24', 'Bonar 2024')


class TestPurchase(unittest.TestCase):
    purchase = transaction.Purchase(today, 2000, ay24, 0.81, euro, "IOL")

    def test_creation(self):
        self.assertEqual(self.purchase.date, today)
        self.assertEqual(self.purchase.financial_instrument, ay24)
        self.assertEqual(self.purchase.security_quantity, 2000)
        self.assertEqual(self.purchase.price, 0.81)
        self.assertEqual(self.purchase.currency, euro)
        self.assertEqual(self.purchase.broker, "IOL")
        self.assertEqual(self.purchase.commissions, 0)
        self.assertEqual(self.purchase.type(), "Compra")

    def test_gross_payment(self):
        self.assertEqual(self.purchase.gross_payment(), 2000 * 0.81)

    def test_signed_quantity(self):
        self.assertEqual(self.purchase.signed_security_quantity(), 2000)


class TestSale(unittest.TestCase):
    sale = transaction.Sale(today, 2000, ay24, 0.81, euro, "IOL")

    def test_creation(self):
        self.assertEqual(self.sale.date, today)
        self.assertEqual(self.sale.financial_instrument, ay24)
        self.assertEqual(self.sale.security_quantity, 2000)
        self.assertEqual(self.sale.price, 0.81)
        self.assertEqual(self.sale.currency, euro)
        self.assertEqual(self.sale.broker, "IOL")
        self.assertEqual(self.sale.commissions, 0)
        self.assertEqual(self.sale.type(), "Venta")

    def test_gross_payment(self):
        self.assertEqual(self.sale.gross_payment(), 2000 * 0.81 * -1)

    def test_signed_quantity(self):
        self.assertEqual(self.sale.signed_security_quantity(), 2000 * -1)


class TestInflow(unittest.TestCase):
    inflow = transaction.Inflow(today, 2000, ay24, "IOL")

    def test_creation(self):
        self.assertEqual(self.inflow.date, today)
        self.assertEqual(self.inflow.financial_instrument, ay24)
        self.assertEqual(self.inflow.security_quantity, 2000)
        self.assertEqual(self.inflow.broker, "IOL")
        self.assertEqual(self.inflow.commissions, 0)
        self.assertEqual(self.inflow.type(), "Ingreso")

    def test_signed_quantity(self):
        self.assertEqual(self.inflow.signed_security_quantity(), 2000)


class TestOutflow(unittest.TestCase):
    outflow = transaction.Outflow(today, 2000, ay24, "IOL")

    def test_creation(self):
        self.assertEqual(self.outflow.date, today)
        self.assertEqual(self.outflow.financial_instrument, ay24)
        self.assertEqual(self.outflow.security_quantity, 2000)
        self.assertEqual(self.outflow.broker, "IOL")
        self.assertEqual(self.outflow.commissions, 0)
        self.assertEqual(self.outflow.type(), "Egreso")

    def test_signed_quantity(self):
        self.assertEqual(self.outflow.signed_security_quantity(), 2000 * -1)


class TestCouponClipping(unittest.TestCase):
    coupon_clipping = transaction.CouponClipping(today, 2000, euro, ay24, "IOL")

    def test_creation(self):
        self.assertEqual(self.coupon_clipping.date, today)
        self.assertEqual(self.coupon_clipping.financial_instrument, euro)
        self.assertEqual(self.coupon_clipping.security_quantity, 2000)
        self.assertEqual(self.coupon_clipping.broker, "IOL")
        self.assertEqual(self.coupon_clipping.commissions, 0)
        self.assertEqual(self.coupon_clipping.referenced_financial_instrument, ay24)
        self.assertEqual(self.coupon_clipping.type(), "Pago de Renta y/o Amortización")

    def test_signed_quantity(self):
        self.assertEqual(self.coupon_clipping.signed_security_quantity(), 2000)


class TestStockDividend(unittest.TestCase):
    stock_dividend = transaction.StockDividend(today, 2000, euro, ay24, "IOL")

    def test_creation(self):
        self.assertEqual(self.stock_dividend.date, today)
        self.assertEqual(self.stock_dividend.financial_instrument, euro)
        self.assertEqual(self.stock_dividend.security_quantity, 2000)
        self.assertEqual(self.stock_dividend.broker, "IOL")
        self.assertEqual(self.stock_dividend.commissions, 0)
        self.assertEqual(self.stock_dividend.referenced_financial_instrument, ay24)
        self.assertEqual(self.stock_dividend.type(), "Pago de Dividendos")

    def test_signed_quantity(self):
        self.assertEqual(self.stock_dividend.signed_security_quantity(), 2000)


if __name__ == '__main__':
    unittest.main()
