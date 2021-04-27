from datetime import (
    date,
)

from my_portfolio_web_app.model.exceptions import InstanceCreationFailed
from my_portfolio_web_app.model.financial_instrument import Currency
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.valuation_system import (
    ValuationSystem,
    ValuationByBruteForce,
    ValuationSourceFromGoogleSheet,
    CurrenciesValuationSource,
    ValuationSourceFromIOLAPI,
)


class ClosingPosition:

    def __init__(self, outflow, security_quantity=None):
        self.outflow = outflow
        if security_quantity is None:
            self.security_quantity = outflow.security_quantity
        else:
            self.security_quantity = security_quantity
        self.assert_security_quantity_within_outflow_quantity()

    def assert_security_quantity_within_outflow_quantity(self):
        if self.security_quantity > self.outflow.security_quantity:
            raise InstanceCreationFailed("Security quantity cannot be more than outflow quantity")

    def __repr__(self):
        return "Imputación de " + self.outflow.financial_instrument.code + " - " + str(self.security_quantity)

    def __eq__(self, other):
        return isinstance(other,
                          ClosingPosition) and self.outflow == other.outflow and self.security_quantity == \
               other.security_quantity

    def date(self):
        return self.outflow.date

    def price(self):
        return self.outflow.price()

    def quantity_on(self, date):
        if date < self.date():
            return 0
        else:
            return self.quantity()

    def alive_quantity_on(self, date):
        if self.outflow.financial_instrument.is_alive_on(date):
            return self.quantity_on(date)
        else:
            return 0

    def quantity(self):
        return Measurement(self.security_quantity, self.outflow.financial_instrument)

    def commissions_on(self, date):
        if date >= self.date():
            return self.outflow.commissions()
        else:
            return 0


class OpenPosition:
    def __init__(self, inflow, closing_positions=None):
        if closing_positions is None:
            closing_positions = []
        self.inflow = inflow
        self.closing_positions = closing_positions
        # TODO: DELETE
        if self.inflow.financial_instrument.code == '$':
            print(self)
            print(inflow)

    def __repr__(self):
        return "Partida de " + self.inflow.financial_instrument.code + " - " + str(
            self.inflow.security_quantity) + " (Remanente " + str(float(self.quantity_on(date.today()))) + ")"

    def __eq__(self, other):
        return isinstance(other,
                          OpenPosition) and self.inflow == other.inflow and self.closing_positions == \
               other.closing_positions

    def date(self):
        return self.inflow.date

    def financial_instrument(self):
        return self.inflow.financial_instrument

    def price(self):
        return self.inflow.price()

    def balance_on(self, date):
        return self.inflow.security_quantity_if_alive_on(date) - self.closing_positions_balance_on(date)

    def quantity_on(self, date):
        if date >= self.date():
            return Measurement(self.inflow.signed_security_quantity(),
                               self.inflow.financial_instrument) - self.closing_positions_quantity_on(date)
        else:
            return 0

    def closing_positions_balance_on(self, date):
        return sum([closing_position.alive_quantity_on(date) for closing_position in self.closing_positions if
                    closing_position.date() <= date])

    def closing_positions_quantity_on(self, date):
        return sum([closing_position.quantity_on(date) for closing_position in self.closing_positions if
                    closing_position.date() <= date])

    def add_closing_position(self, closing_position):
        if self.balance_on(closing_position.date()) >= closing_position.quantity():
            self.closing_positions.append(closing_position)
            # TODO: DELETE
            if self.inflow.financial_instrument.code == '$':
                print(self)
                print(self.inflow)
        else:
            raise InstanceCreationFailed("Cannot add a closing position to this open position")

    def available_quantity_for(self, outflow):
        return min(self.balance_on(outflow.date).value(), outflow.security_quantity)

    def commissions_on(self, date):
        if date >= self.date() and not self.financial_instrument().is_currency():
            return self.inflow.commissions() + sum(
                [closing_position.commissions_on(date) for closing_position in self.closing_positions])
        else:
            return 0


class MonetaryOpenPosition:
    def __init__(self, currency, inflows, outflows):
        self.currency = currency
        self.balance = self.measurements_of(inflows) + self.measurements_of(outflows)
        self.closing_positions = []

    def __repr__(self):
        return "Partida de " + self.financial_instrument().code + " - " + str(self.balance_on(self.date()))

    def measurements_of(self, transactions):
        measurements = []

        for transaction in transactions:
            # If the movement is monetary we just need the commissions
            if transaction.financial_instrument != self.currency:
                measurements.extend(transaction.movements_on(transaction.date).as_bag().non_zero_measurements())
            else:
                measurements.extend((-transaction.commissions()).as_bag().non_zero_measurements())

        return sum([measurement for measurement in measurements if measurement.unit == self.currency])

    @staticmethod
    def ars():
        return Currency.objects.get(code='$')

    @staticmethod
    def date():
        return date.today()

    def financial_instrument(self):
        return self.currency

    def price(self):
        return CurrenciesValuationSource().price_for_on(self.currency, self.ars(), self.date())

    def balance_on(self, date):
        return self.balance - self.closing_positions_balance_on(date)

    def quantity_on(self, date):
        return self.balance_on(date)

    def closing_positions_balance_on(self, date):
        return sum([closing_position.alive_quantity_on(date) for closing_position in self.closing_positions if
                    closing_position.date() <= date])

    def closing_positions_quantity_on(self, date):
        return sum([closing_position.quantity_on(date) for closing_position in self.closing_positions if
                    closing_position.date() <= date])

    def add_closing_position(self, closing_position):
        self.closing_positions.append(closing_position)

    @staticmethod
    def available_quantity_for(outflow):
        return outflow.security_quantity

    @staticmethod
    def commissions_on(date):
        return 0


def add_closing_positions_for_to(outflow, open_positions):
    possible_positions = (open_position for open_position in open_positions if
                          open_position.financial_instrument() == outflow.financial_instrument and
                          outflow.date >= open_position.date())
    remaining_quantity = float(outflow.security_quantity)
    try:
        while remaining_quantity != 0:
            open_position = next(possible_positions)
            affected_quantity = float(min(open_position.available_quantity_for(outflow), remaining_quantity))
            if affected_quantity > 0:
                open_position.add_closing_position(ClosingPosition(outflow, affected_quantity))
            remaining_quantity -= affected_quantity
    except StopIteration:
        raise InstanceCreationFailed("Cannot sell on short")


class OpenPositionCreator:
    def __init__(self, transactions, showing_currencies=False):
        self.showing_currencies = showing_currencies
        self.inflows = [transaction for transaction in transactions if
                        transaction.transaction_sign() == 1 and (
                                showing_currencies or not transaction.financial_instrument.is_currency())]
        self.outflows = [transaction for transaction in transactions if
                         transaction.transaction_sign() == -1 and (
                                 showing_currencies or not transaction.financial_instrument.is_currency())]

    def currencies(self):
        if self.showing_currencies:
            return set(
                [inflow.financial_instrument for inflow in self.inflows if inflow.financial_instrument.is_currency()])
        else:
            return []

    def add_monetary_open_positions(self, open_positions):
        for currency in self.currencies():
            open_positions.append(MonetaryOpenPosition(currency, self.inflows, self.outflows))

    def value(self):
        sorted_open_positions = sorted([OpenPosition(transaction) for transaction in self.inflows],
                                       key=lambda a_open_position: a_open_position.date())
        print(sorted_open_positions)
        self.add_monetary_open_positions(sorted_open_positions)
        print([p for p in sorted_open_positions if p.financial_instrument().code == '$'])
        for outflow in self.outflows:
            add_closing_positions_for_to(outflow, sorted_open_positions)

        open_positions_by_instrument = {}
        for open_position in sorted_open_positions:
            open_positions_by_instrument.setdefault(open_position.financial_instrument(), []).append(open_position)

        return open_positions_by_instrument

    def value_as_list(self):
        return [open_position for open_positions in self.value().values() for open_position in open_positions]


class StockSystem:
    def __init__(self, transactions=None):
        if transactions is None:
            transactions = []
        self.open_positions = OpenPositionCreator(transactions, showing_currencies=True).value()
        self.payments = {}
        for payment_transaction in transactions:
            if payment_transaction.is_payment():
                self.payments.setdefault(payment_transaction.referenced_financial_instrument, []).append(
                    payment_transaction)

    def average_price_for_on(self, financial_instrument, date):
        # TODO: Hacer conversión de monedas
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        if not open_positions:
            return 0
        else:
            prices_for_quantity = [open_position.price() * float(open_position.balance_on(date)) for open_position in
                                   open_positions]
            total_balance = sum([open_position.balance_on(date) for open_position in open_positions])

            return round(sum(prices_for_quantity) / float(total_balance), 8)

    def sales_result_for_on(self, financial_instrument, date):
        # TODO: Hacer conversión de monedas
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum(
            [(closing_position.price() - open_position.price()) * float(closing_position.quantity_on(date)) for
             open_position in open_positions for closing_position in open_position.closing_positions])

    def commissions_result_for_on(self, financial_instrument, date):
        # TODO: Hacer conversión de monedas
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        payments = self.payments.setdefault(financial_instrument, [])
        return -sum([open_position.commissions_on(date) for open_position in open_positions]) - sum(
            [payment.commissions() for payment in payments if payment.date <= date])

    def payments_result_for_on(self, financial_instrument, date):
        # TODO: Hacer conversión de monedas
        payments = self.payments.setdefault(financial_instrument, [])
        return sum([payment.gross_payment() for payment in payments if payment.date <= date])

    def price_difference_result_for_on_using(self, financial_instrument, currency, date, valuation_system):
        # TODO: Hacer conversión de monedas
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum(
            [self.price_difference_result_for_each_on_using(open_position, currency, date, valuation_system)
             for open_position in open_positions])

    @staticmethod
    def price_difference_result_for_each_on_using(open_position, currency, date, valuation_system):
        quantity = open_position.quantity_on(date)
        if quantity != 0:
            return ((valuation_system.valuate_instrument_on(open_position.financial_instrument(), currency,
                                                            date)) - open_position.price()) * float(quantity)
        else:
            return 0

    def current_position_for_on(self, financial_instrument, date):
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum([open_position.balance_on(date) for open_position in open_positions])

    def has_or_had_position_for(self, financial_instrument):
        return self.open_positions.get(financial_instrument) is not None


class InvestmentPerformance:
    def __init__(self, financial_instrument, current_position, average_price, current_price, price_difference_result,
                 payments_result,
                 sales_result, commissions_result):
        self.financial_instrument = financial_instrument
        self.current_position = current_position
        self.average_price = average_price
        self.current_price = current_price
        self.valuated_position = round(self.current_position * self.current_price, 2)
        self.price_difference_result = price_difference_result
        self.payments_result = payments_result
        self.sales_result = sales_result
        self.commissions_result = commissions_result
        self.total = round(price_difference_result + payments_result + sales_result + commissions_result, 2)


class InvestmentPerformanceCalculator:
    def __init__(self, account, financial_instruments, currency, date, broker=None):
        self.account = account
        self.financial_instruments = financial_instruments
        self.currency = currency
        self.date = date
        self.broker = broker
        self.valuation_system = ValuationSystem(
            ValuationByBruteForce(
                [CurrenciesValuationSource(), ValuationSourceFromGoogleSheet(), ValuationSourceFromIOLAPI()]))
        self._stock_system = None

    def stock_system(self):
        if self._stock_system is None:
            if self.broker is None:
                transactions = self.account.registered_transactions()
            else:
                transactions = [transaction for transaction in self.account.registered_transactions() if
                                transaction.broker == self.broker]
            self._stock_system = StockSystem(transactions)
        return self._stock_system

    def instrument_performances(self):
        performances = [InvestmentPerformance(financial_instrument, self.current_position_for(financial_instrument),
                                              self.average_price_for(financial_instrument),
                                              self.current_price_for(financial_instrument),
                                              self.price_differences_result_for(financial_instrument),
                                              self.payments_result_for(financial_instrument),
                                              self.sales_result_for(financial_instrument),
                                              self.commissions_result_for(financial_instrument)) for
                        financial_instrument in self.financial_instruments if
                        self.stock_system().has_or_had_position_for(financial_instrument)]
        return [performance for performance in performances if
                (performance.current_position != 0 or performance.total != 0)]

    def price_for(self, from_currency, to_currency):
        return CurrenciesValuationSource().price_for_on(from_currency, to_currency, self.date)

    def convert_from_to(self, quantity, from_currency, to_currency):
        return quantity * self.price_for(from_currency, to_currency)

    def convert_to(self, amount, currency):
        if amount == 0:
            return Measurement(0, currency)
        else:
            return sum([self.convert_from_to(measurement.quantity, measurement.unit, currency) for measurement in
                        amount.as_bag().non_zero_measurements()])

    @staticmethod
    def round_two_decimals(value):
        return round(value, 2)

    def round_and_convert_to(self, value):
        return self.round_two_decimals(self.convert_to(value, self.currency))

    def current_position_for(self, financial_instrument):
        return self.round_two_decimals(
            float(self.stock_system().current_position_for_on(financial_instrument, self.date)))

    def average_price_for(self, financial_instrument):
        return self.round_and_convert_to(
            self.stock_system().average_price_for_on(financial_instrument, self.date))

    def current_price_for(self, financial_instrument):
        return self.round_and_convert_to(
            self.valuation_system.valuate_instrument_on(financial_instrument, self.currency, self.date))

    def price_differences_result_for(self, financial_instrument):
        return self.round_and_convert_to(
            self.stock_system().price_difference_result_for_on_using(financial_instrument, self.currency,
                                                                     self.date, self.valuation_system))

    def payments_result_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().payments_result_for_on(financial_instrument, self.date))

    def sales_result_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().sales_result_for_on(financial_instrument, self.date))

    def commissions_result_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().commissions_result_for_on(financial_instrument, self.date))
