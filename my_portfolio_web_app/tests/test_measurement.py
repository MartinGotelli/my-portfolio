import unittest
from unittest.mock import Mock

from my_portfolio_web_app.model.measurement import (
    Measurement,
    BagMeasurement,
    NullUnit,
    InvalidMathematicalOperation,
)

ars = Mock()
ars.code = '$'
ars.__eq__ = Mock(side_effect=lambda other: other.code == ars.code)
ars.__hash__ = lambda x: 3
usd = Mock()
usd.code = 'USD'
usd.__eq__ = Mock(side_effect=lambda other: other.code == usd.code)
usd.__hash__ = lambda x: 4

ars_200 = Measurement(200, ars)
null_200 = Measurement(200, NullUnit())
ars_200_plus_null_200 = BagMeasurement([ars_200, null_200])
ars_100 = Measurement(100, ars)
usd_50 = Measurement(50, usd)
ars_100_plus_usd_50 = BagMeasurement([ars_100, usd_50])


class MeasurementTests(unittest.TestCase):
    def test_creation(self):
        self.assertEqual(ars_200.quantity, 200)
        self.assertEqual(ars_200.unit, ars)
        self.assertEqual(ars_200.value(), ars_200.quantity)
        self.assertEqual(str(ars_200), "$ 200")

    def test_equals(self):
        another_amount = Measurement(200, ars)
        self.assertEqual(ars_200, another_amount)
        self.assertEqual(200, null_200)
        self.assertEqual(null_200, 200)
        self.assertNotEqual(null_200, ars_200)
        self.assertEqual(0, Measurement(0, ars))
        self.assertEqual(Measurement(0, ars), 0)

    def test_add(self):
        another_amount = Measurement(200, ars)
        self.assertEqual(ars_200 + another_amount, Measurement(400, ars))
        self.assertEqual(ars_200 + 200, BagMeasurement([ars_200, null_200]))
        self.assertEqual(200 + ars_200, BagMeasurement([ars_200, null_200]))
        self.assertEqual(0 + ars_200, ars_200)
        self.assertEqual(ars_200 + 0, ars_200)
        self.assertEqual(ars_200 + -Measurement(100, ars), Measurement(100, ars))

    def test_subtract(self):
        another_amount = Measurement(100, ars)
        self.assertEqual(ars_200 - another_amount, Measurement(100, ars))
        self.assertEqual(ars_200 - 200, BagMeasurement([ars_200, -null_200]))
        self.assertEqual(300 - ars_200, BagMeasurement([-ars_200, Measurement(300, NullUnit())]))
        self.assertEqual(0 - ars_200, -ars_200)
        self.assertEqual(ars_200 - 0, ars_200)
        self.assertEqual(ars_200 - -200, BagMeasurement([ars_200, null_200]))

    def test_negated(self):
        another_amount = Measurement(-200, ars)
        self.assertEqual(ars_200, -another_amount)
        self.assertEqual(-ars_200, another_amount)

    def test_multiply(self):
        another_amount = Measurement(2, ars)
        with self.assertRaises(InvalidMathematicalOperation):
            ars_200 * another_amount
        self.assertEqual(ars_200 * 2, Measurement(400, ars))
        self.assertEqual(2 * ars_200, Measurement(400, ars))
        self.assertEqual(0 * ars_200, Measurement(0, ars))
        self.assertEqual(ars_200 * -1, -ars_200)

    def test_divide(self):
        another_amount = Measurement(2, ars)
        self.assertEqual(ars_200 / another_amount, Measurement(100, NullUnit()))
        self.assertEqual(ars_200 / 2, Measurement(100, ars))
        with self.assertRaises(InvalidMathematicalOperation):
            200 / ars_200
        self.assertEqual(0 / ars_200, 0)
        self.assertEqual(ars_200 / -1, -ars_200)

    def test_to_int(self):
        self.assertEqual(int(Measurement(2.2, ars)), 2)

    def test_to_float(self):
        self.assertEqual(float(Measurement(2.2, ars)), 2.2)

    def test_max(self):
        max_measurement = Measurement(201, ars)
        self.assertTrue(max_measurement > ars_200)
        self.assertFalse(ars_200 > max_measurement)
        self.assertFalse(ars_200 > ars_200)
        self.assertTrue(ars_200 >= ars_200)
        self.assertNotEqual(max_measurement, ars_200)
        self.assertTrue(201 > null_200)
        self.assertFalse(199 > null_200)
        self.assertTrue(null_200 > 199)
        self.assertFalse(null_200 > 201)
        self.assertTrue(null_200 >= 200)
        self.assertTrue(200 >= null_200)

    def test_min(self):
        min_measurement = Measurement(199, ars)
        self.assertTrue(min_measurement < ars_200)
        self.assertFalse(ars_200 < min_measurement)
        self.assertFalse(ars_200 < ars_200)
        self.assertTrue(ars_200 <= ars_200)
        self.assertNotEqual(min_measurement, ars_200)
        self.assertTrue(199 < null_200)
        self.assertFalse(201 < null_200)
        self.assertTrue(null_200 < 201)
        self.assertFalse(null_200 < 199)
        self.assertTrue(null_200 <= 200)
        self.assertTrue(200 <= null_200)

    def test_as_bag(self):
        self.assertEqual(null_200.as_bag(), BagMeasurement([null_200]))

    def test_iteration(self):
        self.assertEqual([ars_200], [measurement for measurement in ars_200])


class BagMeasurementTest(unittest.TestCase):
    def test_creation(self):
        self.assertEqual(ars_200_plus_null_200.measurements, [ars_200, null_200])
        self.assertEqual(str(ars_200_plus_null_200), "$ 200 + 200")

    def test_equals(self):
        bag = BagMeasurement([ars_200])
        self.assertEqual(ars_200_plus_null_200, bag + 200)
        self.assertEqual(bag + 200, ars_200_plus_null_200)
        self.assertNotEqual(bag, ars_200_plus_null_200)
        self.assertEqual(0, BagMeasurement([]))
        self.assertEqual(BagMeasurement([]), 0)
        self.assertEqual(BagMeasurement([]), Measurement(0, NullUnit))
        self.assertEqual(Measurement(0, NullUnit), BagMeasurement([]))

    def test_add(self):
        bag_of_20_ars = BagMeasurement([Measurement(20, ars)])
        self.assertEqual(ars_200_plus_null_200 + ars_200,
                         BagMeasurement([Measurement(400, ars), null_200]))
        self.assertEqual(ars_200 + ars_200_plus_null_200,
                         BagMeasurement([Measurement(400, ars), null_200]))
        self.assertEqual(ars_200_plus_null_200 + ars_100_plus_usd_50, BagMeasurement(
            [Measurement(300, ars), null_200, Measurement(50, usd)]))
        self.assertEqual(ars_100_plus_usd_50 + ars_200_plus_null_200, BagMeasurement(
            [Measurement(300, ars), null_200, Measurement(50, usd)]))
        self.assertEqual(100 + ars_200_plus_null_200, BagMeasurement([ars_200, Measurement(300, NullUnit())]))
        self.assertEqual(ars_200_plus_null_200 + 100, BagMeasurement([ars_200, Measurement(300, NullUnit())]))
        self.assertEqual(ars_200_plus_null_200 + 0, ars_200_plus_null_200)
        self.assertEqual(0 + ars_200_plus_null_200, ars_200_plus_null_200)
        self.assertEqual(bag_of_20_ars + 0, bag_of_20_ars)
        self.assertEqual(0 + bag_of_20_ars, bag_of_20_ars)
        self.assertEqual(Measurement(0, ars) + 200, null_200)
        self.assertEqual(200 + Measurement(0, ars), null_200)

    def test_subtract(self):
        self.assertEqual(ars_200_plus_null_200 - ars_200,
                         BagMeasurement([null_200]))
        self.assertEqual(ars_200 - ars_200_plus_null_200,
                         BagMeasurement([-null_200]))
        self.assertEqual(ars_200_plus_null_200 - ars_100_plus_usd_50, BagMeasurement(
            [Measurement(100, ars), null_200, Measurement(-50, usd)]))
        self.assertEqual(ars_100_plus_usd_50 - ars_200_plus_null_200, BagMeasurement(
            [Measurement(-100, ars), -null_200, Measurement(50, usd)]))
        self.assertEqual(100 - ars_200_plus_null_200, BagMeasurement([-ars_200, Measurement(-100, NullUnit())]))
        self.assertEqual(ars_200_plus_null_200 - 100, BagMeasurement([ars_200, Measurement(100, NullUnit())]))
        self.assertEqual(ars_200_plus_null_200 - 0, ars_200_plus_null_200)
        self.assertEqual(0 - ars_200_plus_null_200, -ars_200_plus_null_200)

    def test_negated(self):
        negated_bag = BagMeasurement([-ars_200, -null_200])
        self.assertEqual(ars_200_plus_null_200, -negated_bag)
        self.assertEqual(-ars_200_plus_null_200, negated_bag)

    def test_multiply(self):
        self.assertEqual(ars_100_plus_usd_50 * 3, BagMeasurement([ars_100 * 3, usd_50 * 3]))
        self.assertEqual(3 * ars_100_plus_usd_50, BagMeasurement([ars_100 * 3, usd_50 * 3]))
        self.assertEqual(ars_100_plus_usd_50 * 3.22, BagMeasurement([ars_100 * 3.22, usd_50 * 3.22]))
        self.assertEqual(ars_100_plus_usd_50 * 0, 0)
        self.assertEqual(ars_100_plus_usd_50 * Measurement(3, NullUnit()), BagMeasurement([ars_100 * 3, usd_50 * 3]))
        self.assertEqual(Measurement(3, NullUnit()) * ars_100_plus_usd_50, BagMeasurement([ars_100 * 3, usd_50 * 3]))
        with self.assertRaises(InvalidMathematicalOperation):
            ars_100_plus_usd_50 * ars_100_plus_usd_50
        with self.assertRaises(InvalidMathematicalOperation):
            ars_100_plus_usd_50 * ars_100

    def test_divide(self):
        self.assertEqual(ars_100_plus_usd_50 / 2, BagMeasurement([ars_100 / 2, usd_50 / 2]))
        with self.assertRaises(InvalidMathematicalOperation):
            2 / ars_100_plus_usd_50
        self.assertEqual(ars_100_plus_usd_50 / 3.22, BagMeasurement([ars_100 / 3.22, usd_50 / 3.22]))
        self.assertEqual(ars_100_plus_usd_50 / 1, ars_100_plus_usd_50)
        with self.assertRaises(ZeroDivisionError):
            ars_100_plus_usd_50 / 0
        with self.assertRaises(InvalidMathematicalOperation):
            ars_100_plus_usd_50 / ars_100
        self.assertEqual(ars_100_plus_usd_50 / Measurement(2, NullUnit()), BagMeasurement([ars_100 / 2, usd_50 / 2]))
        with self.assertRaises(InvalidMathematicalOperation):
            ars_100_plus_usd_50 * ars_100_plus_usd_50
        with self.assertRaises(InvalidMathematicalOperation):
            ars_100_plus_usd_50 * ars_100

    def test_as_bag(self):
        self.assertEqual(ars_200_plus_null_200.as_bag(), ars_200_plus_null_200)

    def test_iteration(self):
        self.assertEqual(ars_100_plus_usd_50.measurements, [measurement for measurement in ars_100_plus_usd_50])
