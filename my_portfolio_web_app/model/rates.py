from abc import (
    ABC,
    abstractmethod,
)

from my_portfolio_web_app.model.measurement import InvalidMathematicalOperation


class Actual365DayCountBasis:
    def __init__(self, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date

    def __eq__(self, other):
        return isinstance(other, Actual365DayCountBasis) and self.from_date == other.from_date and self.to_date == \
               other.to_date

    def days(self):
        return (self.to_date - self.from_date).days + 1

    def ratio(self):
        return self.days() / self.days_on_year()

    @staticmethod
    def days_on_year():
        return 365


class RateAbstract(ABC):
    def __eq__(self, other):
        return isinstance(other, RateAbstract) and round(other.as_annual_nominal_rate().value(), 8) == round(
            self.as_annual_nominal_rate().value(), 8)

    def __float__(self):
        return float(self.value())

    def __add__(self, other):
        return self.as_annual_nominal_rate() + other

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self.as_annual_nominal_rate() * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.as_annual_nominal_rate() / other

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def ratio(self):
        pass

    @abstractmethod
    def as_annual_nominal_rate(self):
        pass


class Rate(RateAbstract):
    def __init__(self, value, from_date, to_date, day_count_basis_strategy=Actual365DayCountBasis):
        self._value = value
        self.from_date = from_date
        self.to_date = to_date
        self.day_count_basis = day_count_basis_strategy(self.from_date, self.to_date)

    def __repr__(self):
        return f'{self.value() * 100:.2f}% ({self.day_count_basis.days()} días)'

    def value(self):
        return self._value

    def ratio(self):
        return self.day_count_basis.ratio()

    def as_annual_nominal_rate(self):
        value_as_tna = self.value() / self.day_count_basis.ratio()
        return AnnualNominalRate(value_as_tna)


class AnnualNominalRate(RateAbstract):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return f'{self.value() * 100:.2f}% TNA'

    def __add__(self, other):
        if isinstance(other, RateAbstract):
            return AnnualNominalRate(self.value() + other.as_annual_nominal_rate().value())
        elif other == 0:
            return self
        else:
            raise InvalidMathematicalOperation(f'Sum is not supported for numbers {other} and rates {self}')

    def __mul__(self, other):
        if isinstance(other, RateAbstract):
            return AnnualNominalRate(self.value() * other.as_annual_nominal_rate().value())
        else:
            return AnnualNominalRate(self.value() * other)

    def __truediv__(self, other):
        if isinstance(other, RateAbstract):
            return self.value() / other.as_annual_nominal_rate().value()
        else:
            return AnnualNominalRate(self.value() / other)

    def value(self):
        return self._value

    def ratio(self):
        return 1

    def as_annual_nominal_rate(self):
        return self
