from copy import deepcopy
from numbers import Number


def as_measurement(number):
    if isinstance(number, Measurement) or isinstance(number, BagMeasurement):
        return number
    else:
        return Measurement(number, NullUnit())


def is_same_unit(measurement, another):
    return ((isinstance(another, Measurement) and measurement.unit == another.unit) or (
            isinstance(another, Number) and measurement.unit == NullUnit()))


def is_same_unit_or_fail(measurement, another):
    if is_same_unit(measurement, another):
        return True
    else:
        raise InvalidMathematicalOperation("Opearion unsupported, there are different units")


class BagMeasurement:
    def __init__(self, measurements=[]):
        self.measurements = [measurement for measurement in measurements if measurement.value() != 0]

    def __add__(self, other):
        self_copy = deepcopy(self)
        for measurement in self.measurements_from(other):
            self_copy.measurement_of_if_found_if_none(measurement, self_copy.remove_and_add_measurements,
                                                      self_copy.add_new_measurement)
        return self_copy

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self_copy = deepcopy(self)
        for measurement in self.measurements_from(other):
            self_copy.measurement_of_if_found_if_none(measurement, self_copy.remove_and_subtract_measurements,
                                                      self_copy.add_new_negated_measurement)
        return self_copy

    def __rsub__(self, other):
        return -self + other

    def __neg__(self):
        return BagMeasurement([-measurement for measurement in self.measurements])

    def __round__(self, n=None):
        return BagMeasurement([round(measurement, n) for measurement in self.measurements])

    def __eq__(self, other):
        return isinstance(other, self.__class__) and set(self.measurements) == set(
            other.measurements)

    def __repr__(self):
        return "Bolsa de:\n" + '\n'.join(
            [str(measurement) for measurement in self.measurements])

    @staticmethod
    def measurements_from(object):
        if isinstance(object, BagMeasurement):
            return object.non_zero_measurements()
        elif float(object) == 0:
            return []
        elif isinstance(object, Measurement):
            return [object]
        else:
            return [Measurement(object, NullUnit())]

    def non_zero_measurements(self):
        return [measurement for measurement in self.measurements if measurement.value() != 0]

    def measurement_of_if_found_if_none(self, new_measurement, found_method, not_found_method):
        found_measurement = next(
            (measurement for measurement in self.measurements if measurement.unit == new_measurement.unit),
            None)
        if found_measurement is None:
            not_found_method(new_measurement)
        else:
            found_method(found_measurement, new_measurement)

    def remove_and_apply_operator_between_measurements(self, measurement, other_measurement, operator):
        self.assert_same_unit(measurement, other_measurement)
        self.measurements.remove(measurement)
        added_measurement = operator(measurement, other_measurement)
        if added_measurement.value() != 0:
            self.measurements.append(added_measurement)

    def remove_and_add_measurements(self, measurement, other_measurement):
        self.remove_and_apply_operator_between_measurements(measurement, other_measurement, lambda m1, m2: m1 + m2)

    def remove_and_subtract_measurements(self, measurement, other_measurement):
        self.remove_and_apply_operator_between_measurements(measurement, other_measurement, lambda m1, m2: m1 - m2)

    def add_new_measurement(self, measurement):
        self.measurements.append(measurement)

    def add_new_negated_measurement(self, measurement):
        self.add_new_measurement(-measurement)

    @staticmethod
    def assert_same_unit(measurement, other_measurement):
        if measurement.unit != other_measurement.unit:
            raise InvalidMathematicalOperation("There are not the same units")


class NullUnit:
    def __init__(self):
        self.code = "N/A"

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class Measurement:
    def __init__(self, quantity, unit):
        self.quantity = quantity
        self.unit = unit

    def __add__(self, other):
        if isinstance(other, BagMeasurement):
            return other + self
        elif float(other) == 0:
            return self
        elif self.value() == 0:
            return as_measurement(other)
        elif not is_same_unit(self, other):
            return BagMeasurement([self]) + other
        else:
            return Measurement(self.value() + float(other), self.unit)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, BagMeasurement):
            return -other + self
        elif float(other) == 0:
            return self
        elif not is_same_unit(self, other):
            return BagMeasurement([self]) - other
        else:
            return Measurement(self.value() - float(other), self.unit)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, Number) or (isinstance(other, Measurement) and other.unit == NullUnit()):
            return Measurement(self.value() * float(other), self.unit)
        else:
            self.not_supported_operation('Multiplication')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if float(self) == 0:
            return 0
        elif isinstance(other, Number) or (isinstance(other, Measurement) and other.unit == NullUnit()):
            return Measurement(self.value() / float(other), self.unit)
        elif isinstance(other, Measurement) and other.unit == self.unit:
            return Measurement(self.value() / float(other), NullUnit())
        else:
            self.not_supported_operation('Division')

    def __rtruediv__(self, other):
        if float(other) == 0:
            return 0
        elif (isinstance(other, Number) and self.unit == NullUnit()) or (
                isinstance(other, Measurement) and self.unit == other.unit):
            return Measurement(float(other) / self.value(), NullUnit())
        else:
            self.not_supported_operation('Division')

    def __lt__(self, other):
        return is_same_unit_or_fail(self, other) and float(self) < float(other)

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return is_same_unit_or_fail(self, other) and float(self) > float(other)

    def __ge__(self, other):
        return self == other or self > other

    def __eq__(self, other):
        return (float(self) == 0 and float(other) == 0) or is_same_unit(self, other) and float(self) == float(other)

    def __hash__(self):
        return hash((float(self.quantity), self.unit))

    def __repr__(self):
        return self.unit.code + ' ' + str(self.quantity)

    def __int__(self):
        return int(self.value())

    def __float__(self):
        return float(self.value())

    def __neg__(self):
        return Measurement(-self.value(), self.unit)

    def __round__(self, n=None):
        return Measurement(round(self.value(), n), self.unit)

    def not_supported_operation(self, operation):
        raise InvalidMathematicalOperation(operation + ' is not supported for this units')

    def value(self):
        return self.quantity


class InvalidMathematicalOperation(Exception):
    pass
