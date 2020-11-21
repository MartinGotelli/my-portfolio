import unittest
import datetime

from model.exceptions import InstanceCreationFailed
from model.financial_instrument import Bond, Currency, Stock
from model.measurement import Measurement
from model.stock_system import OpenPosition, ClosingPosition, OpenPositionCreator, StockSystem
from model.transaction import Purchase, Inflow, Sale

euro = Currency('EUR', 'Euro')
one_euro = Measurement(1, euro)
today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)
ay24 = Bond('AY24', 'Bonar 2024', tomorrow)
purchase = Purchase(today, 2000, ay24, Measurement(0.81, euro), "IOL")
purchase_1200 = Purchase(today, 1200, ay24, Measurement(0.81, euro), "IOL")
purchase_10000 = Purchase(tomorrow, 10000, ay24, 0.78 * one_euro, "IOL")
today_sale = sale = Sale(today, 500, ay24, Measurement(0.83, euro), "IOL")
sale = Sale(tomorrow, 500, ay24, Measurement(0.83, euro), "IOL")
sale_2000 = Sale(tomorrow, 2000, ay24, Measurement(0.83, euro), "IOL")
deposit_1000 = Inflow(today, 1000, euro, "IOL")
closing_position_500 = ClosingPosition(sale)
closing_position_200 = ClosingPosition(sale, 200)
closing_position_2000 = ClosingPosition(sale_2000)
open_position_1500 = OpenPosition(purchase, [closing_position_500])
meli = Stock("MELI", "MERCADOLIBRE")


class TestClosingPosition(unittest.TestCase):
    def test_creation(self):
        closing_position = ClosingPosition(sale, 200)
        self.assertEqual(closing_position.outflow, sale)
        self.assertEqual(closing_position.security_quantity, 200)
        self.assertEqual(closing_position.date(), sale.date)
        self.assertEqual(str(closing_position), "Imputación de AY24 - 200")
        closing_position = ClosingPosition(sale)
        self.assertEqual(closing_position.outflow, sale)
        self.assertEqual(closing_position.security_quantity, 500)
        self.assertEqual(closing_position.date(), sale.date)
        self.assertEqual(str(closing_position), "Imputación de AY24 - 500")

    def test_security_quantity_exceeds_sale_quantity(self):
        ClosingPosition(sale, 499)
        ClosingPosition(sale, 500)
        with self.assertRaises(InstanceCreationFailed):
            ClosingPosition(sale, 501)
        with self.assertRaises(InstanceCreationFailed):
            ClosingPosition(sale, 1000)

    def test_quantity_on(self):
        self.assertEqual(closing_position_500.quantity_on(sale.date), Measurement(500, ay24))
        self.assertEqual(closing_position_500.quantity_on(sale.date), closing_position_500.quantity())
        self.assertEqual(closing_position_500.quantity_on(today), 0)


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
