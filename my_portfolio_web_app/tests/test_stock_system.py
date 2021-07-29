import datetime

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from my_portfolio_web_app.model.exceptions import InstanceCreationFailed
from my_portfolio_web_app.model.financial_instrument import (
    Bond,
    Currency,
    Stock,
)
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.rates import Rate
from my_portfolio_web_app.model.stock_system import (
    ClosingPosition,
    OpenPosition,
    OpenPositionCreator,
    StockSystem,
)
from my_portfolio_web_app.model.transaction import (
    CouponClipping,
    Inflow,
    Purchase,
    Sale,
    StockDividend,
)
from my_portfolio_web_app.model.valuation_system import (
    ValuationSourceFromDictionary,
    ValuationSystem,
)

yesterday = datetime.date(2020, 2, 1)
today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)


def create_if_not_exists(model, search_by, **kwargs):
    if search_by not in kwargs:
        AssertionError('Search by not included in kwargs!')
    search_value = kwargs[search_by]
    search_dict = {search_by: search_value}
    objects = model.objects.filter(**search_dict)
    if len(objects) == 0:
        return model.objects.create(**kwargs)
    else:
        return objects[0]


def ars():
    return create_if_not_exists(Currency, search_by='code', code='$', description='Pesos')


def one_ars():
    return Measurement(1, ars())


def ay24():
    return create_if_not_exists(Bond, search_by='code', code='AY24', description='Bonar 2024', maturity_date=tomorrow)


def meli():
    return create_if_not_exists(Stock, search_by='code', code='MELI', description='MercadoLibre')


def valuation_system():
    valuation_source = ValuationSourceFromDictionary({
        today: {
            ay24(): [0.82 * one_ars()],
        },
        tomorrow: {
            ay24(): [0.85 * one_ars()]
        },
        after_tomorrow: {
            ay24(): [0.90 * one_ars()]
        }
    })

    return ValuationSystem(valuation_source)


def account():
    return create_if_not_exists(InvestmentIndividualAccount, search_by='description', description='Test Account')


def _sale():
    return Sale.objects.create(date=tomorrow, security_quantity=500, financial_instrument=ay24(),
                               price=Measurement(0.83, ars()), broker="IOL", commissions=4 * one_ars(),
                               account=account())


def _today_sale():
    return Sale.objects.create(date=today, security_quantity=500, financial_instrument=ay24(),
                               price=Measurement(0.825, ars()), broker="IOL", commissions=3.5 * one_ars(),
                               account=account())


def _purchase():
    return Purchase.objects.create(date=today, security_quantity=2000, financial_instrument=ay24(),
                                   price=Measurement(0.81, ars()), broker="IOL", commissions=10 * one_ars(),
                                   account=account())


def _sale_2000():
    return Sale.objects.create(date=tomorrow, security_quantity=2000, financial_instrument=ay24(),
                               price=Measurement(0.84, ars()), broker="IOL", commissions=7.5 * one_ars(),
                               account=account())


def _deposit_1000():
    return Inflow(date=today, security_quantity=1000, financial_instrument=ars(), broker="IOL")


def _purchase_10000():
    return Purchase(date=tomorrow, security_quantity=10000, financial_instrument=ay24(), price=0.78 * one_ars(),
                    broker="IOL", commissions=100 * one_ars())


def _purchase_1200():
    return Purchase(date=today, security_quantity=1200, financial_instrument=ay24(), price=Measurement(0.81, ars()),
                    broker="IOL", commissions=8 * one_ars())


def _coupon_clipping():
    return CouponClipping(date=tomorrow, security_quantity=550, financial_instrument=ars(),
                          referenced_financial_instrument=ay24(), broker="IOL", commissions=20 * one_ars())


class TestClosingPosition(TestCase):
    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()

    def test_creation(self):
        sale = _sale()
        closing_position = ClosingPosition(sale, 200)
        self.assertEqual(closing_position.outflow, sale)
        self.assertEqual(closing_position.security_quantity, 200)
        self.assertEqual(closing_position.date(), sale.date)
        self.assertEqual(closing_position.price(), sale.price())
        self.assertEqual(str(closing_position), "Imputación de AY24 - 200")
        closing_position = ClosingPosition(sale)
        self.assertEqual(closing_position.outflow, sale)
        self.assertEqual(closing_position.security_quantity, 500)
        self.assertEqual(closing_position.date(), sale.date)
        self.assertEqual(closing_position.price(), sale.price())
        self.assertEqual(str(closing_position), "Imputación de AY24 - 500")

    def test_security_quantity_exceeds_sale_quantity(self):
        sale = _sale()
        ClosingPosition(sale, 499)
        ClosingPosition(sale, 500)
        with self.assertRaises(InstanceCreationFailed):
            ClosingPosition(sale, 501)
        with self.assertRaises(InstanceCreationFailed):
            ClosingPosition(sale, 1000)

    def test_quantity_on(self):
        ay24_200 = Measurement(200, ay24())
        ay24_500 = Measurement(500, ay24())
        sale = _sale()
        today_sale = _today_sale()
        closing_position_200 = ClosingPosition(sale, 200)
        self.assertEqual(closing_position_200.quantity_on(sale.date), ay24_200)
        self.assertEqual(closing_position_200.quantity_on(sale.date), closing_position_200.quantity())
        self.assertEqual(closing_position_200.quantity_on(today), 0)
        # AY24 not alive after tomorrow
        self.assertEqual(closing_position_200.quantity_on(after_tomorrow), ay24_200)
        closing_position = ClosingPosition(today_sale)
        self.assertEqual(closing_position.quantity_on(today), ay24_500)
        self.assertEqual(closing_position.quantity_on(tomorrow), ay24_500)
        # AY24 not alive after tomorrow
        self.assertEqual(closing_position.quantity_on(after_tomorrow), ay24_500)

    def test_alive_quantity_on(self):
        ay24_200 = Measurement(200, ay24())
        ay24_500 = Measurement(500, ay24())
        sale = _sale()
        today_sale = _today_sale()
        closing_position_200 = ClosingPosition(sale, 200)
        self.assertEqual(closing_position_200.alive_quantity_on(sale.date), ay24_200)
        self.assertEqual(closing_position_200.alive_quantity_on(sale.date), closing_position_200.quantity())
        self.assertEqual(closing_position_200.alive_quantity_on(today), 0)
        # AY24 not alive after tomorrow
        self.assertEqual(closing_position_200.alive_quantity_on(after_tomorrow), 0)
        closing_position = ClosingPosition(today_sale)
        self.assertEqual(closing_position.alive_quantity_on(today), ay24_500)
        self.assertEqual(closing_position.alive_quantity_on(tomorrow), ay24_500)
        # AY24 not alive after tomorrow
        self.assertEqual(closing_position.alive_quantity_on(after_tomorrow), 0)


class TestOpenPosition(TestCase):
    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()

    def test_creation(self):
        purchase = _purchase()
        open_position = OpenPosition(purchase, [])
        self.assertEqual(open_position.inflow, purchase)
        self.assertEqual(open_position.closing_positions, [])
        self.assertEqual(open_position.date(), purchase.date)
        self.assertEqual(open_position.financial_instrument(), purchase.financial_instrument)
        self.assertEqual(open_position.price(), purchase.price())
        self.assertEqual(str(open_position), "Partida de AY24 - 2000 (Remanente 2000.0)")

    def test_add_closing_position(self):
        purchase = _purchase()
        closing_position_200 = ClosingPosition(_sale(), 200)
        open_position = OpenPosition(purchase, [])
        self.assertEqual(open_position.closing_positions, [])
        open_position.add_closing_position(closing_position_200)
        self.assertEqual(open_position.closing_positions, [closing_position_200])

    def test_add_closing_position_exceeding_balance_value(self):
        purchase = _purchase()
        closing_position_200 = ClosingPosition(_sale(), 200)
        closing_position_2000 = ClosingPosition(_sale_2000(), 2000)
        open_position = OpenPosition(purchase, [closing_position_2000])
        self.assertEqual(open_position.closing_positions, [closing_position_2000])
        with self.assertRaises(InstanceCreationFailed):
            open_position.add_closing_position(closing_position_200)

    def test_balance_on_without_closing_positions(self):
        purchase = _purchase()
        open_position = OpenPosition(purchase, [])
        self.assertEqual(open_position.balance_on(today), Measurement(2000, ay24()))
        self.assertEqual(open_position.balance_on(after_tomorrow), 0)

    def test_balance_on_with_one_closing_position(self):
        open_position_1500 = OpenPosition(_purchase(), [ClosingPosition(_sale_2000(), 500)])
        self.assertEqual(open_position_1500.balance_on(today), Measurement(2000, ay24()))
        self.assertEqual(open_position_1500.balance_on(tomorrow), Measurement(1500, ay24()))
        self.assertEqual(open_position_1500.balance_on(after_tomorrow), 0)

    def test_gross_payment_on(self):
        open_position_1500 = OpenPosition(_purchase(), [ClosingPosition(_sale_2000(), 500)])
        self.assertEqual(open_position_1500.gross_payment_on(today), Measurement(2000 * 0.81, ars()))
        self.assertEqual(open_position_1500.gross_payment_on(tomorrow), Measurement(1500 * 0.81, ars()))
        self.assertEqual(open_position_1500.gross_payment_on(after_tomorrow), 0)

    def test_quantity_on(self):
        open_position_1500 = OpenPosition(_purchase(), [ClosingPosition(_sale_2000(), 500)])
        self.assertEqual(open_position_1500.quantity_on(yesterday), 0)
        self.assertEqual(open_position_1500.quantity_on(today), Measurement(2000, ay24()))
        self.assertEqual(open_position_1500.quantity_on(tomorrow), Measurement(1500, ay24()))
        self.assertEqual(open_position_1500.quantity_on(after_tomorrow), Measurement(1500, ay24()))


class TestOpenPositionCreator(TestCase):
    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()

    def test_creation(self):
        purchase = _purchase()
        sale = _sale()
        creator = OpenPositionCreator([purchase, sale, _deposit_1000()])
        self.assertEqual(creator.inflows, [purchase])
        self.assertEqual(creator.outflows, [sale])

    def test_open_positions_without_closings(self):
        purchase = _purchase()
        purchase_10000 = _purchase_10000()
        creator = OpenPositionCreator([purchase, purchase_10000])
        self.assertEqual(creator.value()[ay24()], [OpenPosition(purchase), OpenPosition(purchase_10000)])

    def test_open_positions_without_closings_sorts_by_date(self):
        purchase = _purchase()
        purchase_10000 = _purchase_10000()
        creator = OpenPositionCreator([purchase_10000, purchase])
        self.assertEqual(creator.value()[ay24()], [OpenPosition(purchase), OpenPosition(purchase_10000)])

    def test_open_position_with_one_closing(self):
        purchase = _purchase()
        sale = _sale()
        closing_position_500 = ClosingPosition(sale, 500)
        creator = OpenPositionCreator([purchase, sale])
        self.assertEqual(creator.value()[ay24()], [OpenPosition(purchase, [closing_position_500])])

    def test_open_position_with_multiple_closings(self):
        purchase = _purchase()
        sale = _sale()
        closing_position_500 = ClosingPosition(sale, 500)
        creator = OpenPositionCreator([purchase, sale, sale])
        self.assertEqual(creator.value()[ay24()],
                         [OpenPosition(purchase, [closing_position_500, closing_position_500])])

    def test_closing_position_in_two_open_positions(self):
        purchase_1200 = _purchase_1200()
        sale_2000 = _sale_2000()
        creator = OpenPositionCreator([purchase_1200, purchase_1200, sale_2000])
        self.assertEqual(creator.value()[ay24()], [OpenPosition(purchase_1200, [ClosingPosition(sale_2000, 1200)]),
                                                   OpenPosition(purchase_1200, [ClosingPosition(sale_2000, 800)])])

    def test_exceeding_open_position_balance(self):
        # A.K.A. selling short
        creator = OpenPositionCreator([_purchase_1200(), _sale_2000()])
        with self.assertRaises(InstanceCreationFailed):
            creator.value()

    def test_purchase_of_tomorrow_unaffected_by_today_sale(self):
        creator = OpenPositionCreator([_purchase_10000(), _today_sale()])
        with self.assertRaises(InstanceCreationFailed):
            creator.value()


class TestStockSystem(TestCase):
    def setUp(self):
        super().setUp()
        ContentType.objects.clear_cache()

    def test_creation(self):
        purchase = _purchase()
        stock_system = StockSystem()
        self.assertEqual(stock_system.open_positions, {})
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])

    def test_average_price_for_on(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.average_price_for_on(ay24(), tomorrow), 0.81 * one_ars())

    def test_average_price_for_absent_instrument(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.average_price_for_on(meli(), tomorrow), 0)

    def test_average_price_for_completely_sold_position(self):
        purchase = _purchase()
        sale_2000 = _sale_2000()
        stock_system = StockSystem([purchase, sale_2000])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale_2000)])])
        self.assertEqual(
            stock_system.average_price_for_on(ay24(), tomorrow), 0)

    def test_average_price_for_multiple_purchase(self):
        purchase = _purchase()
        purchase_10000 = _purchase_10000()
        stock_system = StockSystem([purchase, purchase_10000])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase), OpenPosition(purchase_10000)])
        self.assertEqual(
            stock_system.average_price_for_on(ay24(), tomorrow), (2000 * 0.81 + 10000 * 0.78) / 12000 * one_ars())

    def test_average_price_for_multiple_purchase_and_sales(self):
        purchase = _purchase()
        purchase_10000 = _purchase_10000()
        sale = _sale()
        stock_system = StockSystem([purchase, purchase_10000, sale])
        self.assertEqual(stock_system.open_positions[ay24()],
                         [OpenPosition(purchase, [ClosingPosition(sale)]), OpenPosition(purchase_10000)])
        self.assertEqual(
            stock_system.average_price_for_on(ay24(), tomorrow),
            round(((2000 - 500) * 0.81 + 10000 * 0.78) / (12000 - 500) * one_ars(), 8))

    def test_sales_result_for_on(self):
        purchase = _purchase()
        sale = _sale()
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale)])])
        self.assertEqual(stock_system.sales_result_for_on(ay24(), today), 0)
        self.assertEqual(stock_system.sales_result_for_on(ay24(), sale.date),
                         (0.83 - 0.81) * float(sale.security_quantity) * one_ars())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.sales_result_for_on(ay24(), after_tomorrow),
                         (0.83 - 0.81) * float(sale.security_quantity) * one_ars())

    def test_sales_result_for_on_without_outflows(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.sales_result_for_on(ay24(), tomorrow), 0)

    def test_sales_result_for_multiple_open_positions(self):
        purchase = _purchase()
        sale = _sale()
        sale_2000 = _sale_2000()
        stock_system = StockSystem([purchase, sale_2000, purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale_2000)]),
                                                               OpenPosition(purchase, [ClosingPosition(sale)])])
        self.assertEqual(stock_system.sales_result_for_on(ay24(), today), 0)
        self.assertEqual(stock_system.sales_result_for_on(ay24(), sale.date),
                         ((0.84 - 0.81) * float(sale_2000.security_quantity) + (
                                 0.83 - 0.81) * float(sale.security_quantity)) * one_ars())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.sales_result_for_on(ay24(), after_tomorrow),
                         ((0.84 - 0.81) * float(sale_2000.security_quantity) + (
                                 0.83 - 0.81) * float(sale.security_quantity)) * one_ars())

    def test_sales_result_for_multiple_closing_positions(self):
        purchase = _purchase()
        sale = _sale()
        today_sale = _today_sale()
        stock_system = StockSystem([purchase, today_sale, sale])
        self.assertEqual(stock_system.open_positions[ay24()],
                         [OpenPosition(purchase, [ClosingPosition(today_sale), ClosingPosition(sale)])])
        self.assertEqual(stock_system.sales_result_for_on(ay24(), today),
                         (0.825 - 0.81) * float(today_sale.security_quantity) * one_ars())
        self.assertEqual(stock_system.sales_result_for_on(ay24(), sale.date),
                         ((0.825 - 0.81) * float(today_sale.security_quantity) + (
                                 0.83 - 0.81) * float(sale.security_quantity)) * one_ars())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.sales_result_for_on(ay24(), after_tomorrow),
                         ((0.825 - 0.81) * float(today_sale.security_quantity) + (
                                 0.83 - 0.81) * float(sale.security_quantity)) * one_ars())

    def test_commissions_result_for_on(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), today), -purchase.commissions())
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), tomorrow), -purchase.commissions())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), after_tomorrow), -purchase.commissions())

    def test_commissions_result_for_multiple_open_positions(self):
        purchase = _purchase()
        purchase_10000 = _purchase_10000()
        stock_system = StockSystem([purchase, purchase_10000])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase), OpenPosition(purchase_10000)])
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), today), -purchase.commissions())
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), tomorrow),
                         -purchase.commissions() - purchase_10000.commissions())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), after_tomorrow),
                         -purchase.commissions() - purchase_10000.commissions())

    def test_commissions_result_for_one_closing_position(self):
        purchase = _purchase()
        sale = _sale()
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale)])])
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), today), -purchase.commissions())
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), tomorrow),
                         -purchase.commissions() - sale.commissions())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), after_tomorrow),
                         -purchase.commissions() - sale.commissions())

    def test_commissions_result_for_multiple_closing_positions(self):
        purchase = _purchase()
        sale = _sale()
        today_sale = _today_sale()
        stock_system = StockSystem([purchase, today_sale, sale])
        self.assertEqual(stock_system.open_positions[ay24()],
                         [OpenPosition(purchase, [ClosingPosition(today_sale), ClosingPosition(sale)])])
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), today),
                         -purchase.commissions() - today_sale.commissions())
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), tomorrow),
                         -purchase.commissions() - sale.commissions() - today_sale.commissions())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), after_tomorrow),
                         -purchase.commissions() - sale.commissions() - today_sale.commissions())

    def test_commissions_result_for_payments(self):
        purchase = _purchase()
        coupon_clipping = _coupon_clipping()
        stock_system = StockSystem([purchase, coupon_clipping])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.payments[ay24()], [coupon_clipping])
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), today),
                         -purchase.commissions())
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), tomorrow),
                         -purchase.commissions() - coupon_clipping.commissions())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24(), after_tomorrow),
                         -purchase.commissions() - coupon_clipping.commissions())

    def test_payments_result_for_on(self):
        coupon_clipping = _coupon_clipping()
        stock_system = StockSystem([])
        self.assertEqual(stock_system.payments_result_for_on(ay24(), today), 0)
        stock_system = StockSystem([coupon_clipping])
        self.assertEqual(stock_system.payments[ay24()], [coupon_clipping])
        self.assertEqual(stock_system.payments_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24(), today), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24(), tomorrow),
                         coupon_clipping.gross_payment())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.payments_result_for_on(ay24(), after_tomorrow),
                         coupon_clipping.gross_payment())

    def test_payments_result_for_multiple_coupon_clippings(self):
        coupon_clipping = _coupon_clipping()
        coupon_clipping_200 = CouponClipping(date=today, security_quantity=200, financial_instrument=ars(),
                                             referenced_financial_instrument=ay24(), broker="IOL")
        coupon_clipping_meli = CouponClipping(date=today, security_quantity=350, financial_instrument=ars(),
                                              referenced_financial_instrument=meli(), broker="IOL")
        stock_system = StockSystem([coupon_clipping, coupon_clipping_200, coupon_clipping_meli])
        self.assertEqual(stock_system.payments[ay24()], [coupon_clipping, coupon_clipping_200])
        self.assertEqual(stock_system.payments[meli()], [coupon_clipping_meli])
        self.assertEqual(stock_system.payments_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(meli(), yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24(), today),
                         coupon_clipping_200.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(meli(), today),
                         coupon_clipping_meli.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(ay24(), tomorrow),
                         coupon_clipping.gross_payment() + coupon_clipping_200.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(meli(), tomorrow),
                         coupon_clipping_meli.gross_payment())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.payments_result_for_on(ay24(), after_tomorrow),
                         coupon_clipping.gross_payment() + coupon_clipping_200.gross_payment())

    def test_payments_result_for_dividends_payment(self):
        coupon_clipping = _coupon_clipping()
        dividends_payment = StockDividend(date=today, security_quantity=200, financial_instrument=ars(),
                                          referenced_financial_instrument=ay24(), broker="IOL")
        stock_system = StockSystem([coupon_clipping, dividends_payment])
        self.assertEqual(stock_system.payments[ay24()], [coupon_clipping, dividends_payment])
        self.assertEqual(stock_system.payments_result_for_on(ay24(), yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24(), today),
                         dividends_payment.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(ay24(), tomorrow),
                         coupon_clipping.gross_payment() + dividends_payment.gross_payment())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.payments_result_for_on(ay24(), after_tomorrow),
                         coupon_clipping.gross_payment() + dividends_payment.gross_payment())

    def test_price_difference_result_for_on_using(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(
            stock_system.price_difference_result_for_on_using(ay24(), ars(), yesterday, valuation_system()), 0)
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24(), ars(), today, valuation_system()),
                         (0.82 - 0.81) * 2000 * one_ars())
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24(), ars(), tomorrow, valuation_system()),
                         (0.85 - 0.81) * 2000 * one_ars())
        # AY24 is not alive anymore
        self.assertEqual(
            stock_system.price_difference_result_for_on_using(ay24(), ars(), after_tomorrow, valuation_system()),
            (0.90 - 0.81) * 2000 * one_ars())

    def test_price_difference_result_for_purchase_with_closing_positions(self):
        purchase = _purchase()
        sale = _sale()
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale)])])
        self.assertEqual(
            stock_system.price_difference_result_for_on_using(ay24(), ars(), yesterday, valuation_system()), 0)
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24(), ars(), today, valuation_system()),
                         (0.82 - 0.81) * 2000 * one_ars())
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24(), ars(), tomorrow, valuation_system()),
                         (0.85 - 0.81) * 1500 * one_ars())
        # AY24 is not alive anymore
        self.assertEqual(
            stock_system.price_difference_result_for_on_using(ay24(), ars(), after_tomorrow, valuation_system()),
            (0.90 - 0.81) * 1500 * one_ars())

    def test_performance_percentage_for_price_difference(self):
        purchase = Purchase.objects.create(date=today, security_quantity=2000, financial_instrument=ay24(),
                                           price=Measurement(0.81, ars()), broker="IOL", account=account())
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate(((0.85 - 0.81) * 2000) / (0.81 * 2000), today, tomorrow))

    def test_performance_percentage_for_price_difference_and_commissions(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), today, valuation_system()),
                         Rate((((0.82 - 0.81) * 2000) - 10) / (0.81 * 2000), today, today))
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate((((0.85 - 0.81) * 2000) - 10) / (0.81 * 2000), today, tomorrow))

    def test_performance_percentage_for_full_sale(self):
        purchase = _purchase()
        sale_2000 = _sale_2000()
        stock_system = StockSystem([purchase, sale_2000])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale_2000)])])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), today, valuation_system()),
                         Rate((((0.82 - 0.81) * 2000) - 10) / (0.81 * 2000), today, today))
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate((((0.84 - 0.81) * 2000) - 10 - 7.5) / (0.81 * 2000), today, tomorrow))

    def test_performance_percentage_for_partial_sale(self):
        purchase = _purchase()
        sale = _sale()
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase, [ClosingPosition(sale)])])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), today, valuation_system()),
                         Rate((((0.82 - 0.81) * 2000) - 10) / (0.81 * 2000), today, today))
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate((((0.85 - 0.81) * 1500 + (0.83 - 0.81) * 500 - 10 - 4) / (0.81 * 2000)), today, tomorrow))

    def test_performance_with_multiple_purchases(self):
        purchase = _purchase()
        stock_system = StockSystem([purchase, purchase])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase), OpenPosition(purchase)])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), today, valuation_system()),
                         Rate((((0.82 - 0.81) * 2000) - 10) / (0.81 * 2000), today, today))
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate((((0.85 - 0.81) * 2000) - 10) / (0.81 * 2000), today, tomorrow))

    def test_performance_with_multiple_purchases_and_sales(self):
        purchase = _purchase()
        sale = _sale()
        stock_system = StockSystem([purchase, purchase, sale, sale])
        self.assertEqual(stock_system.open_positions[ay24()],
                         [OpenPosition(purchase, [ClosingPosition(sale), ClosingPosition(sale)]),
                          OpenPosition(purchase)])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), today, valuation_system()),
                         Rate((((0.82 - 0.81) * 2000) - 10) / (0.81 * 2000), today, today))
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate(((0.85 - 0.81) * 3000 + (0.83 - 0.81) * 1000 - 10 * 2 - 4 * 2) / (0.81 * 4000), today,
                              tomorrow))

    def test_performance_with_payments(self):
        purchase = _purchase()
        coupon_clipping = _coupon_clipping()
        stock_system = StockSystem([purchase, coupon_clipping])
        self.assertEqual(stock_system.open_positions[ay24()], [OpenPosition(purchase)])
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), today, valuation_system()),
                         Rate(((0.82 - 0.81) * 2000 - 10) / (0.81 * 2000), today, today))
        self.assertEqual(stock_system.performance_rate(ay24(), ars(), tomorrow, valuation_system()),
                         Rate(((0.85 - 0.81) * 2000 - 10 + (550 - 20)) / (0.81 * 2000), today, tomorrow))
