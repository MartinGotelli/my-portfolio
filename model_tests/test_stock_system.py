import unittest
import datetime

from model.exceptions import InstanceCreationFailed
from model.financial_instrument import Bond, Currency, Stock
from model.measurement import Measurement
from model.stock_system import OpenPosition, ClosingPosition, OpenPositionCreator, StockSystem
from model.transaction import Purchase, Inflow, Sale, CouponClipping, StockDividend
from model.valuation_system import ValuationSystem, ValuationSourceFromDictionary

euro = Currency('EUR', 'Euro')
one_euro = Measurement(1, euro)
yesterday = datetime.date(2020, 2, 1)
today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)
ay24 = Bond('AY24', 'Bonar 2024', tomorrow)
purchase = Purchase(today, 2000, ay24, Measurement(0.81, euro), "IOL", 10 * one_euro)
purchase_1200 = Purchase(today, 1200, ay24, Measurement(0.81, euro), "IOL", 8 * one_euro)
purchase_10000 = Purchase(tomorrow, 10000, ay24, 0.78 * one_euro, "IOL", 100 * one_euro)
today_sale = Sale(today, 500, ay24, Measurement(0.825, euro), "IOL", 3.5 * one_euro)
sale = Sale(tomorrow, 500, ay24, Measurement(0.83, euro), "IOL", 4 * one_euro)
sale_2000 = Sale(tomorrow, 2000, ay24, Measurement(0.84, euro), "IOL", 7.5 * one_euro)
deposit_1000 = Inflow(today, 1000, euro, "IOL")
coupon_clipping = CouponClipping(tomorrow, 550, euro, ay24, "IOL", 20 * one_euro)
closing_position_500 = ClosingPosition(sale)
closing_position_200 = ClosingPosition(sale, 200)
closing_position_2000 = ClosingPosition(sale_2000)
open_position_1500 = OpenPosition(purchase, [closing_position_500])
meli = Stock("MELI", "MERCADOLIBRE")

valuation_source = ValuationSourceFromDictionary({
    today: {
        ay24: [0.82 * one_euro],
    },
    tomorrow: {
        ay24: [0.85 * one_euro]
    },
    after_tomorrow: {
        ay24: [0.90 * one_euro]
    }
})

valuation_system = ValuationSystem(valuation_source)


class TestClosingPosition(unittest.TestCase):
    def test_creation(self):
        closing_position = ClosingPosition(sale, 200)
        self.assertEqual(closing_position.outflow, sale)
        self.assertEqual(closing_position.security_quantity, 200)
        self.assertEqual(closing_position.date(), sale.date)
        self.assertEqual(closing_position.price(), sale.price)
        self.assertEqual(str(closing_position), "Imputación de AY24 - 200")
        closing_position = ClosingPosition(sale)
        self.assertEqual(closing_position.outflow, sale)
        self.assertEqual(closing_position.security_quantity, 500)
        self.assertEqual(closing_position.date(), sale.date)
        self.assertEqual(closing_position.price(), sale.price)
        self.assertEqual(str(closing_position), "Imputación de AY24 - 500")

    def test_security_quantity_exceeds_sale_quantity(self):
        ClosingPosition(sale, 499)
        ClosingPosition(sale, 500)
        with self.assertRaises(InstanceCreationFailed):
            ClosingPosition(sale, 501)
        with self.assertRaises(InstanceCreationFailed):
            ClosingPosition(sale, 1000)

    def test_quantity_on(self):
        ay24_200 = Measurement(200, ay24)
        ay24_500 = Measurement(500, ay24)
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
        ay24_200 = Measurement(200, ay24)
        ay24_500 = Measurement(500, ay24)
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


class TestOpenPosition(unittest.TestCase):
    def test_creation(self):
        open_position = OpenPosition(purchase, [])
        self.assertEqual(open_position.inflow, purchase)
        self.assertEqual(open_position.closing_positions, [])
        self.assertEqual(open_position.date(), purchase.date)
        self.assertEqual(open_position.financial_instrument(), purchase.financial_instrument)
        self.assertEqual(open_position.price(), purchase.price)
        self.assertEqual(str(open_position), "Partida de AY24 - 2000")

    def test_add_closing_position(self):
        open_position = OpenPosition(purchase, [])
        self.assertEqual(open_position.closing_positions, [])
        open_position.add_closing_position(closing_position_200)
        self.assertEqual(open_position.closing_positions, [closing_position_200])

    def test_add_closing_position_exceeding_balance_value(self):
        open_position = OpenPosition(purchase, [closing_position_2000])
        self.assertEqual(open_position.closing_positions, [closing_position_2000])
        with self.assertRaises(InstanceCreationFailed):
            open_position.add_closing_position(closing_position_200)

    def test_balance_on_without_closing_positions(self):
        open_position = OpenPosition(purchase, [])
        self.assertEqual(open_position.balance_on(today), Measurement(2000, ay24))
        self.assertEqual(open_position.balance_on(after_tomorrow), 0)

    def test_balance_on_with_one_closing_position(self):
        self.assertEqual(open_position_1500.balance_on(today), Measurement(2000, ay24))
        self.assertEqual(open_position_1500.balance_on(tomorrow), Measurement(1500, ay24))
        self.assertEqual(open_position_1500.balance_on(after_tomorrow), 0)

    def test_quantity_on(self):
        self.assertEqual(open_position_1500.quantity_on(yesterday), 0)
        self.assertEqual(open_position_1500.quantity_on(today), Measurement(2000, ay24))
        self.assertEqual(open_position_1500.quantity_on(tomorrow), Measurement(1500, ay24))
        self.assertEqual(open_position_1500.quantity_on(after_tomorrow), Measurement(1500, ay24))


class TestOpenPositionCreator(unittest.TestCase):
    def test_creation(self):
        creator = OpenPositionCreator([purchase, sale, deposit_1000])
        self.assertEqual(creator.inflows, [purchase])
        self.assertEqual(creator.outflows, [sale])

    def test_open_positions_without_closings(self):
        creator = OpenPositionCreator([purchase, purchase_10000])
        self.assertEqual(creator.value()[ay24], [OpenPosition(purchase), OpenPosition(purchase_10000)])

    def test_open_positions_without_closings_sorts_by_date(self):
        creator = OpenPositionCreator([purchase_10000, purchase])
        self.assertEqual(creator.value()[ay24], [OpenPosition(purchase), OpenPosition(purchase_10000)])

    def test_open_position_with_one_closing(self):
        creator = OpenPositionCreator([purchase, sale])
        self.assertEqual(creator.value()[ay24], [OpenPosition(purchase, [closing_position_500])])

    def test_open_position_with_multiple_closings(self):
        creator = OpenPositionCreator([purchase, sale, sale])
        self.assertEqual(creator.value()[ay24],
                         [OpenPosition(purchase, [closing_position_500, closing_position_500])])

    def test_closing_position_in_two_open_positions(self):
        creator = OpenPositionCreator([purchase_1200, purchase_1200, sale_2000])
        self.assertEqual(creator.value()[ay24], [OpenPosition(purchase_1200, [ClosingPosition(sale_2000, 1200)]),
                                                 OpenPosition(purchase_1200, [ClosingPosition(sale_2000, 800)])])

    def test_exceeding_open_position_balance(self):
        # A.K.A. selling short
        creator = OpenPositionCreator([purchase_1200, sale_2000])
        with self.assertRaises(InstanceCreationFailed):
            creator.value()

    def test_purchase_of_tomorrow_unaffected_by_today_sale(self):
        creator = OpenPositionCreator([purchase_10000, today_sale])
        with self.assertRaises(InstanceCreationFailed):
            creator.value()


class TestStockSystem(unittest.TestCase):
    def test_creation(self):
        stock_system = StockSystem()
        self.assertEqual(stock_system.open_positions, {})
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])

    def test_average_price_for_on(self):
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])
        self.assertEqual(stock_system.average_price_for_on(ay24, tomorrow), 0.81 * one_euro)

    def test_average_price_for_absent_instrument(self):
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])
        self.assertEqual(stock_system.average_price_for_on(meli, tomorrow), 0)

    def test_average_price_for_completely_sold_position(self):
        stock_system = StockSystem([purchase, sale_2000])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase, [closing_position_2000])])
        self.assertEqual(
            stock_system.average_price_for_on(ay24, tomorrow), 0)

    def test_average_price_for_multiple_purchase(self):
        stock_system = StockSystem([purchase, purchase_10000])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase), OpenPosition(purchase_10000)])
        self.assertEqual(
            stock_system.average_price_for_on(ay24, tomorrow), (2000 * 0.81 + 10000 * 0.78) / 12000 * one_euro)

    def test_average_price_for_multiple_purchase_and_sales(self):
        stock_system = StockSystem([purchase, purchase_10000, sale])
        self.assertEqual(stock_system.open_positions[ay24],
                         [OpenPosition(purchase, [closing_position_500]), OpenPosition(purchase_10000)])
        self.assertEqual(
            stock_system.average_price_for_on(ay24, tomorrow),
            round(((2000 - 500) * 0.81 + 10000 * 0.78) / (12000 - 500) * one_euro, 8))

    def test_sales_result_for_on(self):
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24], [open_position_1500])
        self.assertEqual(stock_system.sales_result_for_on(ay24, today), 0)
        self.assertEqual(stock_system.sales_result_for_on(ay24, sale.date),
                         (0.83 - 0.81) * sale.security_quantity * one_euro)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.sales_result_for_on(ay24, after_tomorrow),
                         (0.83 - 0.81) * sale.security_quantity * one_euro)

    def test_sales_result_for_on_without_outflows(self):
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])
        self.assertEqual(stock_system.sales_result_for_on(ay24, tomorrow), 0)

    def test_sales_result_for_multiple_open_positions(self):
        stock_system = StockSystem([purchase, sale_2000, purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24],
                         [OpenPosition(purchase, [closing_position_2000]), open_position_1500])
        self.assertEqual(stock_system.sales_result_for_on(ay24, today), 0)
        self.assertEqual(stock_system.sales_result_for_on(ay24, sale.date),
                         ((0.84 - 0.81) * sale_2000.security_quantity + (
                                 0.83 - 0.81) * sale.security_quantity) * one_euro)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.sales_result_for_on(ay24, after_tomorrow),
                         ((0.84 - 0.81) * sale_2000.security_quantity + (
                                 0.83 - 0.81) * sale.security_quantity) * one_euro)

    def test_sales_result_for_multiple_closing_positions(self):
        stock_system = StockSystem([purchase, today_sale, sale])
        self.assertEqual(stock_system.open_positions[ay24],
                         [OpenPosition(purchase, [ClosingPosition(today_sale), closing_position_500])])
        self.assertEqual(stock_system.sales_result_for_on(ay24, today),
                         (0.825 - 0.81) * today_sale.security_quantity * one_euro)
        self.assertEqual(stock_system.sales_result_for_on(ay24, sale.date),
                         ((0.825 - 0.81) * today_sale.security_quantity + (
                                 0.83 - 0.81) * sale.security_quantity) * one_euro)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.sales_result_for_on(ay24, after_tomorrow),
                         ((0.825 - 0.81) * today_sale.security_quantity + (
                                 0.83 - 0.81) * sale.security_quantity) * one_euro)

    def test_commissions_result_for_on(self):
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])
        self.assertEqual(stock_system.commissions_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, today), -purchase.commissions)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, tomorrow), -purchase.commissions)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24, after_tomorrow), -purchase.commissions)

    def test_commissions_result_for_multiple_open_positions(self):
        stock_system = StockSystem([purchase, purchase_10000])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase), OpenPosition(purchase_10000)])
        self.assertEqual(stock_system.commissions_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, today), -purchase.commissions)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, tomorrow),
                         -purchase.commissions - purchase_10000.commissions)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24, after_tomorrow),
                         -purchase.commissions - purchase_10000.commissions)

    def test_commissions_result_for_one_closing_position(self):
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24], [open_position_1500])
        self.assertEqual(stock_system.commissions_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, today), -purchase.commissions)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, tomorrow),
                         -purchase.commissions - sale.commissions)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24, after_tomorrow),
                         -purchase.commissions - sale.commissions)

    def test_commissions_result_for_multiple_closing_positions(self):
        stock_system = StockSystem([purchase, today_sale, sale])
        self.assertEqual(stock_system.open_positions[ay24],
                         [OpenPosition(purchase, [ClosingPosition(today_sale), closing_position_500])])
        self.assertEqual(stock_system.commissions_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, today),
                         -purchase.commissions - today_sale.commissions)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, tomorrow),
                         -purchase.commissions - sale.commissions - today_sale.commissions)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24, after_tomorrow),
                         -purchase.commissions - sale.commissions - today_sale.commissions)

    def test_commissions_result_for_payments(self):
        stock_system = StockSystem([purchase, coupon_clipping])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])
        self.assertEqual(stock_system.payments[ay24], [coupon_clipping])
        self.assertEqual(stock_system.commissions_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, today),
                         -purchase.commissions)
        self.assertEqual(stock_system.commissions_result_for_on(ay24, tomorrow),
                         -purchase.commissions - coupon_clipping.commissions)
        # AY24 is not alive anymore
        self.assertEqual(stock_system.commissions_result_for_on(ay24, after_tomorrow),
                         -purchase.commissions - coupon_clipping.commissions)

    def test_payments_result_for_on(self):
        stock_system = StockSystem([])
        self.assertEqual(stock_system.payments_result_for_on(ay24, today), 0)
        stock_system = StockSystem([coupon_clipping])
        self.assertEqual(stock_system.payments[ay24], [coupon_clipping])
        self.assertEqual(stock_system.payments_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24, today), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24, tomorrow),
                         coupon_clipping.gross_payment())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.payments_result_for_on(ay24, after_tomorrow),
                         coupon_clipping.gross_payment())

    def test_payments_result_for_multiple_coupon_clippings(self):
        coupon_clipping_200 = CouponClipping(today, 200, euro, ay24, "IOL")
        coupon_clipping_meli = CouponClipping(today, 350, euro, meli, "IOL")
        stock_system = StockSystem([coupon_clipping, coupon_clipping_200, coupon_clipping_meli])
        self.assertEqual(stock_system.payments[ay24], [coupon_clipping, coupon_clipping_200])
        self.assertEqual(stock_system.payments[meli], [coupon_clipping_meli])
        self.assertEqual(stock_system.payments_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(meli, yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24, today),
                         coupon_clipping_200.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(meli, today),
                         coupon_clipping_meli.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(ay24, tomorrow),
                         coupon_clipping.gross_payment() + coupon_clipping_200.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(meli, tomorrow),
                         coupon_clipping_meli.gross_payment())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.payments_result_for_on(ay24, after_tomorrow),
                         coupon_clipping.gross_payment() + coupon_clipping_200.gross_payment())

    def test_payments_result_for_dividends_payment(self):
        dividends_payment = StockDividend(today, 200, euro, ay24, "IOL")
        stock_system = StockSystem([coupon_clipping, dividends_payment])
        self.assertEqual(stock_system.payments[ay24], [coupon_clipping, dividends_payment])
        self.assertEqual(stock_system.payments_result_for_on(ay24, yesterday), 0)
        self.assertEqual(stock_system.payments_result_for_on(ay24, today),
                         dividends_payment.gross_payment())
        self.assertEqual(stock_system.payments_result_for_on(ay24, tomorrow),
                         coupon_clipping.gross_payment() + dividends_payment.gross_payment())
        # AY24 is not alive anymore
        self.assertEqual(stock_system.payments_result_for_on(ay24, after_tomorrow),
                         coupon_clipping.gross_payment() + dividends_payment.gross_payment())

    def test_price_difference_result_for_on_using(self):
        stock_system = StockSystem([purchase])
        self.assertEqual(stock_system.open_positions[ay24], [OpenPosition(purchase)])
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24, euro, yesterday, valuation_system), 0)
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24, euro, today, valuation_system),
                         (0.82 - 0.81) * 2000 * one_euro)
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24, euro, tomorrow, valuation_system),
                         (0.85 - 0.81) * 2000 * one_euro)
        # AY24 is not alive anymore
        self.assertEqual(
            stock_system.price_difference_result_for_on_using(ay24, euro, after_tomorrow, valuation_system),
            (0.90 - 0.81) * 2000 * one_euro)

    def test_price_difference_result_for_purchase_with_closing_positions(self):
        stock_system = StockSystem([purchase, sale])
        self.assertEqual(stock_system.open_positions[ay24], [open_position_1500])
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24, euro, yesterday, valuation_system), 0)
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24, euro, today, valuation_system),
                         (0.82 - 0.81) * 2000 * one_euro)
        self.assertEqual(stock_system.price_difference_result_for_on_using(ay24, euro, tomorrow, valuation_system),
                         (0.85 - 0.81) * 1500 * one_euro)
        # AY24 is not alive anymore
        self.assertEqual(
            stock_system.price_difference_result_for_on_using(ay24, euro, after_tomorrow, valuation_system),
            (0.90 - 0.81) * 1500 * one_euro)
