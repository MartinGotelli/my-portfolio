import datetime
from unittest import TestCase

from my_portfolio_web_app.model.rates import (
    Actual365DayCountBasis,
    AnnualNominalRate,
    Rate,
)

today = datetime.date(2020, 2, 2)
tomorrow = datetime.date(2020, 2, 3)
after_tomorrow = datetime.date(2020, 2, 4)


class TestActual360DayCountBasis(TestCase):
    def test_creation(self):
        day_count_basis = Actual365DayCountBasis(today, after_tomorrow)
        self.assertEqual(day_count_basis.from_date, today)
        self.assertEqual(day_count_basis.to_date, after_tomorrow)

    def test_days(self):
        day_count_basis = Actual365DayCountBasis(today, after_tomorrow)
        self.assertEqual(day_count_basis.days(), (after_tomorrow - today).days + 1)
        day_count_basis = Actual365DayCountBasis(today, datetime.date(2021, 2, 4))
        self.assertEqual(day_count_basis.days(), 367 + 2)

    def test_days_on_year(self):
        day_count_basis = Actual365DayCountBasis(today, after_tomorrow)
        self.assertEqual(day_count_basis.days_on_year(), 365)

    def test_ratio(self):
        day_count_basis = Actual365DayCountBasis(today, after_tomorrow)
        self.assertEqual(day_count_basis.ratio(), 3 / 365)
        day_count_basis = Actual365DayCountBasis(today, datetime.date(2021, 2, 4))
        self.assertEqual(day_count_basis.ratio(), 369 / 365)


class TestRate(TestCase):
    def test_creation(self):
        rate = Rate(0.03, today, after_tomorrow)
        self.assertEqual(rate.value(), 0.03)
        self.assertEqual(rate.from_date, today)
        self.assertEqual(rate.to_date, after_tomorrow)
        self.assertEqual(rate.day_count_basis, Actual365DayCountBasis(today, after_tomorrow))
        self.assertEqual(str(rate), '3.00% (3 días)')

    def test_equality(self):
        rate = Rate(0.03, today, after_tomorrow)
        another_rate = Rate(0.03, today, after_tomorrow)
        different_rate = Rate(0.03, today, tomorrow)
        an_rate = AnnualNominalRate(0.03 / rate.day_count_basis.ratio())
        self.assertEqual(rate, another_rate)
        self.assertNotEqual(rate, different_rate)
        self.assertEqual(rate, an_rate)

    def test_as_annual_nominal_rate(self):
        rate = Rate(0.03, today, after_tomorrow)
        an_rate = rate.as_annual_nominal_rate()
        self.assertEqual(rate, an_rate)
        self.assertAlmostEqual(an_rate.value(), 0.03 * 365 / 3)

    def test_multiplication(self):
        rate = Rate(0.03, today, after_tomorrow)
        an_rate = AnnualNominalRate(0.03)
        self.assertEqual(rate * 3, AnnualNominalRate((0.03 * 365 / 3) * 3))
        self.assertEqual(3 * rate, AnnualNominalRate((0.03 * 365 / 3) * 3))
        self.assertEqual(rate * 0, AnnualNominalRate(0))
        self.assertEqual(rate * an_rate, AnnualNominalRate((0.03 * 365 / 3) * 0.03))
        self.assertEqual(an_rate * rate, AnnualNominalRate((0.03 * 365 / 3) * 0.03))

    def test_division(self):
        rate = Rate(0.03, today, after_tomorrow)
        an_rate = AnnualNominalRate(0.03)
        self.assertEqual(rate / 3, AnnualNominalRate((0.03 * 365 / 3) / 3))
        self.assertEqual(rate / 1, AnnualNominalRate((0.03 * 365 / 3)))
        self.assertAlmostEqual(rate / an_rate, (0.03 * 365 / 3) / 0.03)


class TestAnnualNominalRate(TestCase):
    def test_creation(self):
        rate = AnnualNominalRate(0.03)
        self.assertEqual(rate.value(), 0.03)
        self.assertEqual(str(rate), '3.00% TNA')

    def test_as_annual_nominal_rate(self):
        rate = AnnualNominalRate(0.03)
        an_rate = rate.as_annual_nominal_rate()
        self.assertEqual(rate, an_rate)
        self.assertEqual(an_rate.value(), 0.03)

    def test_multiplication(self):
        rate = AnnualNominalRate(0.03)
        self.assertEqual(rate * 3, AnnualNominalRate(0.03 * 3))
        self.assertEqual(3 * rate, AnnualNominalRate(0.03 * 3))
        self.assertEqual(rate * 0, AnnualNominalRate(0))

    def test_division(self):
        rate = AnnualNominalRate(0.03)
        self.assertEqual(rate / 3, AnnualNominalRate(0.03 / 3))
        self.assertEqual(rate / 1, AnnualNominalRate(0.03))
