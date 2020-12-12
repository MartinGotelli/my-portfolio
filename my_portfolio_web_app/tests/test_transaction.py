import datetime

from django.test import TestCase

from my_portfolio_web_app.model.financial_instrument import ars, Currency, Bond, usd
from my_portfolio_web_app.model.measurement import Measurement, NullUnit
from my_portfolio_web_app.model.transaction import Purchase, Sale, Inflow, Outflow, CouponClipping, StockDividend

euro = Currency(code='EUR', description='Euro')
today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)
ay24 = Bond(code='AY24', description='Bonar 2024', maturity_date=tomorrow)


def assert_movements_for_using(transaction, test_case):
    test_case.assertEqual(transaction.movements_on(today), transaction.security_quantity_if_alive_on(
        today) - transaction.gross_payment() - transaction.commissions())


def assert_security_quantity_if_alive_on_for_using(transaction, test_case):
    security_quantity = Measurement(transaction.signed_security_quantity(), transaction.financial_instrument)

    test_case.assertEqual(transaction.security_quantity_if_alive_on(today), security_quantity
                          )
    test_case.assertEqual(transaction.security_quantity_if_alive_on(tomorrow),
                          security_quantity)
    if not transaction.financial_instrument.is_alive_on(after_tomorrow):
        security_quantity = 0

    test_case.assertEqual(transaction.security_quantity_if_alive_on(after_tomorrow),
                          security_quantity)


class TestPurchase(TestCase):
    purchase = Purchase(date=today, security_quantity=2000, financial_instrument=ay24, price_amount=0.81,
                        price_unit=euro, broker="IOL")

    def test_creation(self):
        self.assertEqual(self.purchase.date, today)
        self.assertEqual(self.purchase.financial_instrument, ay24)
        self.assertEqual(self.purchase.security_quantity, 2000)
        self.assertEqual(self.purchase.price().value(), 0.81)
        self.assertEqual(self.purchase.price().unit, euro)
        self.assertEqual(self.purchase.broker, "IOL")
        self.assertEqual(self.purchase.ars_commissions, 0)
        self.assertEqual(self.purchase.usd_commissions, 0)
        self.assertEqual(self.purchase.commissions(), 0)
        self.assertEqual(self.purchase.type, "Compra")

    def test_creation_with_price_and_commissions_as_measurements(self):
        purchase = Purchase(date=today, security_quantity=2000, financial_instrument=ay24,
                            price=Measurement(0.81, euro), broker="IOL",
                            commissions=Measurement(100, ars) + Measurement(3, usd))
        self.assertEqual(purchase.date, today)
        self.assertEqual(purchase.financial_instrument, ay24)
        self.assertEqual(purchase.security_quantity, 2000)
        self.assertEqual(purchase.price().value(), 0.81)
        self.assertEqual(purchase.price_amount, 0.81)
        self.assertEqual(purchase.price().unit, euro)
        self.assertEqual(purchase.price_unit, euro)
        self.assertEqual(purchase.broker, "IOL")
        self.assertEqual(purchase.ars_commissions, 100)
        self.assertEqual(purchase.usd_commissions, 3)
        self.assertEqual(purchase.commissions(), Measurement(100, ars) + Measurement(3, usd))
        self.assertEqual(purchase.type, "Compra")

    def test_gross_payment(self):
        self.assertEqual(self.purchase.gross_payment(), Measurement(2000 * 0.81, euro))

    def test_signed_quantity(self):
        self.assertEqual(self.purchase.signed_security_quantity(), 2000)

    def test_currency(self):
        self.assertEqual(self.purchase.currency(), euro)

    def test_security_quantity_if_alive_on(self):
        assert_security_quantity_if_alive_on_for_using(self.purchase, self)

    def test_movements_on(self):
        assert_movements_for_using(self.purchase, self)


class TestSale(TestCase):
    sale = Sale(date=today, security_quantity=2000, financial_instrument=ay24, price=Measurement(0.81, euro),
                broker="IOL")

    def test_creation(self):
        self.assertEqual(self.sale.date, today)
        self.assertEqual(self.sale.financial_instrument, ay24)
        self.assertEqual(self.sale.security_quantity, 2000)
        self.assertEqual(self.sale.price().value(), 0.81)
        self.assertEqual(self.sale.price().unit, euro)
        self.assertEqual(self.sale.broker, "IOL")
        self.assertEqual(self.sale.ars_commissions, 0)
        self.assertEqual(self.sale.usd_commissions, 0)
        self.assertEqual(self.sale.commissions(), 0)
        self.assertEqual(self.sale.type, "Venta")

    def test_gross_payment(self):
        self.assertEqual(self.sale.gross_payment(), Measurement(2000 * 0.81 * -1, euro))

    def test_signed_quantity(self):
        self.assertEqual(self.sale.signed_security_quantity(), 2000 * -1)

    def test_currency(self):
        self.assertEqual(self.sale.currency(), euro)

    def test_security_quantity_if_alive_on(self):
        assert_security_quantity_if_alive_on_for_using(self.sale, self)

    def test_movements_on(self):
        assert_movements_for_using(self.sale, self)


class TestInflow(TestCase):
    inflow = Inflow(date=today, security_quantity=2000, financial_instrument=ay24, broker="IOL")

    def test_creation(self):
        self.assertEqual(self.inflow.date, today)
        self.assertEqual(self.inflow.financial_instrument, ay24)
        self.assertEqual(self.inflow.security_quantity, 2000)
        self.assertEqual(self.inflow.broker, "IOL")
        self.assertEqual(self.inflow.ars_commissions, 0)
        self.assertEqual(self.inflow.usd_commissions, 0)
        self.assertEqual(self.inflow.commissions(), 0)
        self.assertEqual(self.inflow.type, "Ingreso")
        self.assertEqual(self.inflow.price(), 0)
        self.assertEqual(self.inflow.price().unit, NullUnit())

    def test_signed_quantity(self):
        self.assertEqual(self.inflow.signed_security_quantity(), 2000)

    def test_security_quantity_if_alive_on(self):
        assert_security_quantity_if_alive_on_for_using(self.inflow, self)

    def test_movements_on(self):
        assert_movements_for_using(self.inflow, self)


class TestOutflow(TestCase):
    outflow = Outflow(date=today, security_quantity=2000, financial_instrument=ay24, broker="IOL")

    def test_creation(self):
        self.assertEqual(self.outflow.date, today)
        self.assertEqual(self.outflow.financial_instrument, ay24)
        self.assertEqual(self.outflow.security_quantity, 2000)
        self.assertEqual(self.outflow.broker, "IOL")
        self.assertEqual(self.outflow.ars_commissions, 0)
        self.assertEqual(self.outflow.usd_commissions, 0)
        self.assertEqual(self.outflow.commissions(), 0)
        self.assertEqual(self.outflow.type, "Egreso")
        self.assertEqual(self.outflow.price(), 0)
        self.assertEqual(self.outflow.price().unit, NullUnit())

    def test_signed_quantity(self):
        self.assertEqual(self.outflow.signed_security_quantity(), 2000 * -1)

    def test_security_quantity_if_alive_on(self):
        assert_security_quantity_if_alive_on_for_using(self.outflow, self)

    def test_movements_on(self):
        assert_movements_for_using(self.outflow, self)


class TestCouponClipping(TestCase):
    coupon_clipping = CouponClipping(date=today, security_quantity=2000, financial_instrument=euro,
                                     referenced_financial_instrument=ay24, broker="IOL")

    def test_creation(self):
        self.assertEqual(self.coupon_clipping.date, today)
        self.assertEqual(self.coupon_clipping.financial_instrument, euro)
        self.assertEqual(self.coupon_clipping.security_quantity, 2000)
        self.assertEqual(self.coupon_clipping.broker, "IOL")
        self.assertEqual(self.coupon_clipping.ars_commissions, 0)
        self.assertEqual(self.coupon_clipping.usd_commissions, 0)
        self.assertEqual(self.coupon_clipping.commissions(), 0)
        self.assertEqual(self.coupon_clipping.referenced_financial_instrument, ay24)
        self.assertEqual(self.coupon_clipping.type, "Pago de Renta y/o Amortización")

    def test_signed_quantity(self):
        self.assertEqual(self.coupon_clipping.signed_security_quantity(), 2000)

    def test_security_quantity_if_alive_on(self):
        assert_security_quantity_if_alive_on_for_using(self.coupon_clipping, self)

    def test_movements_on(self):
        assert_movements_for_using(self.coupon_clipping, self)

    def test_gross_payment(self):
        self.assertEqual(self.coupon_clipping.gross_payment(), Measurement(2000, euro))


class TestStockDividend(TestCase):
    stock_dividend = StockDividend(date=today, security_quantity=2000, financial_instrument=euro,
                                   referenced_financial_instrument=ay24, broker="IOL")

    def test_creation(self):
        self.assertEqual(self.stock_dividend.date, today)
        self.assertEqual(self.stock_dividend.financial_instrument, euro)
        self.assertEqual(self.stock_dividend.security_quantity, 2000)
        self.assertEqual(self.stock_dividend.broker, "IOL")
        self.assertEqual(self.stock_dividend.ars_commissions, 0)
        self.assertEqual(self.stock_dividend.usd_commissions, 0)
        self.assertEqual(self.stock_dividend.commissions(), 0)
        self.assertEqual(self.stock_dividend.referenced_financial_instrument, ay24)
        self.assertEqual(self.stock_dividend.type, "Pago de Dividendos")

    def test_signed_quantity(self):
        self.assertEqual(self.stock_dividend.signed_security_quantity(), 2000)

    def test_security_quantity_if_alive_on(self):
        assert_security_quantity_if_alive_on_for_using(self.stock_dividend, self)

    def test_movements_on(self):
        assert_movements_for_using(self.stock_dividend, self)

    def test_gross_payment(self):
        self.assertEqual(self.stock_dividend.gross_payment(), Measurement(2000, euro))
