from datetime import (
    date,
)

from my_portfolio_web_app.model.exceptions import InstanceCreationFailed
from my_portfolio_web_app.model.financial_instrument import Currency
from my_portfolio_web_app.model.measurement import Measurement
from my_portfolio_web_app.model.rates import Rate
from my_portfolio_web_app.model.transaction_manager import TransactionManager
from my_portfolio_web_app.model.valuation_system import (
    CurrenciesValuationSource,
    MoneyConverter,
    ValuationByBruteForce,
    ValuationSourceFromGoogleSheet,
    ValuationSourceFromIOLAPI,
    ValuationSystem,
)


def convert_to(amount, currency, date):
    return MoneyConverter(currency, date).convert_to(amount, currency)


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

    def __repr__(self):
        return "Partida de " + self.inflow.financial_instrument.code + " - " + str(
            self.inflow.security_quantity) + " (Remanente " + str(float(self.quantity_on(date.today()))) + ")"

    def __eq__(self, other):
        return isinstance(other,
                          OpenPosition) and self.inflow == other.inflow and self.closing_positions == \
               other.closing_positions

    def date(self):
        return self.inflow.date

    def closing_date(self):
        if self.closing_positions:
            max_closing_position_date = max(closing_position.date() for closing_position in self.closing_positions)
        else:
            max_closing_position_date = self.date()

        if self.balance_on(max_closing_position_date) == 0:
            return max_closing_position_date
        else:
            return None

    def financial_instrument(self):
        return self.inflow.financial_instrument

    def price(self):
        return self.inflow.price()

    def balance_on(self, date):
        return self.inflow.security_quantity_if_alive_on(date) - self.closing_positions_balance_on(date)

    def gross_payment_on(self, date=None):
        if not date:
            date = self.date()
        return self.price() * self.balance_on(date).quantity

    def security_quantity(self):
        return self.inflow.security_quantity

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
            measurements.extend(
                transaction.monetary_movements_on(transaction.date).as_bag().non_zero_measurements())

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

    def gross_payment_on(self, date=None):
        return 0

    def quantity_on(self, date):
        return self.balance_on(date)

    def security_quantity(self):
        return 0

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
        sorted_open_positions = sorted([OpenPosition(transaction) for transaction in self.inflows if
                                        not transaction.financial_instrument.is_currency()],
                                       key=lambda a_open_position: a_open_position.date())
        self.add_monetary_open_positions(sorted_open_positions)
        for outflow in self.outflows:
            if not outflow.financial_instrument.is_currency():
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
            if total_balance == 0:
                return 0
            else:
                return round(sum(prices_for_quantity) / float(total_balance), 8)

    def sales_result_for_on(self, financial_instrument, date):
        # TODO: Hacer conversión de monedas
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum([self.position_sales_result(open_position, date) for open_position in open_positions])

    @staticmethod
    def position_sales_result(open_position, date):
        return sum([(closing_position.price() - open_position.price()) * float(closing_position.quantity_on(date)) for
                    closing_position in open_position.closing_positions])

    def commissions_result_for_on(self, financial_instrument, date):
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        payments = self.payments.setdefault(financial_instrument, [])
        return sum([self.position_commissions_result(open_position, date) for open_position in open_positions]) - sum(
            [payment.commissions() for payment in payments if payment.date <= date])

    @staticmethod
    def position_commissions_result(open_position, date):
        return -open_position.commissions_on(date)

    def payments_result_for_on(self, financial_instrument, date):
        payments = self.payments.setdefault(financial_instrument, [])
        return sum([payment.gross_payment() for payment in payments if payment.date <= date])

    def position_payments_result(self, open_position, currency, date):
        payments = self.payments.setdefault(open_position.financial_instrument(), [])
        return float(sum([convert_to(payment.monetary_movements(), currency, date) * float(open_position.balance_on(
            payment.date)) / float(self.current_position_for_on(open_position.financial_instrument(), payment.date)) for
                          payment in payments if payment.date <= date]))

    def price_difference_result_for_on_using(self, financial_instrument, currency, date, valuation_system):
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum(
            [self.position_price_difference_result(open_position, currency, date, valuation_system)
             for open_position in open_positions])

    @staticmethod
    def position_price_difference_result(open_position, currency, date, valuation_system):
        quantity = open_position.quantity_on(date)
        if quantity != 0:
            return ((valuation_system.valuate_instrument_on(open_position.financial_instrument(), currency,
                                                            date)) - open_position.price()) * float(quantity)
        else:
            return 0

    def performance_rate(self, financial_instrument, currency, date, valuation_system):
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        total_position = float(
            sum([open_position.balance_on(open_position.date()) for open_position in open_positions]))
        return sum([self.position_weighted_performance_percentage(open_position, currency, date, valuation_system,
                                                                  total_position) for
                    open_position in open_positions])

    def position_weighted_performance_percentage(self, open_position, currency, date, valuation_system, total_position):
        if isinstance(open_position, MonetaryOpenPosition):
            # TODO: CAMBIAR
            return 0

        initial_balance = float(open_position.balance_on(open_position.date()))

        performance_percentage = self.position_performance_rate(open_position, currency, date, valuation_system)

        if total_position == 0 or performance_percentage == 0:
            return performance_percentage
        else:
            return performance_percentage * initial_balance / total_position

    def position_performance_rate(self, open_position, currency, date, valuation_system):
        initial_gross_payment = float(convert_to(open_position.gross_payment_on(), currency, date))

        if initial_gross_payment == 0:
            # TODO: Handlea el caso de IRC9O
            return 0

        sales_result_percentage = float(
            convert_to(self.position_sales_result(open_position, date) / initial_gross_payment, currency, date))
        commissions_result_percentage = float(
            convert_to(self.position_commissions_result(open_position, date) / initial_gross_payment, currency, date))
        price_difference_result_percentage = float(convert_to(
            self.position_price_difference_result(open_position, currency, date,
                                                  valuation_system) / initial_gross_payment, currency, date))
        payments_result_percentage = float(
            self.position_payments_result(open_position, currency, date) / initial_gross_payment)

        return Rate(float(
            sales_result_percentage + commissions_result_percentage + price_difference_result_percentage +
            payments_result_percentage),
            open_position.date(), date)

    def total_investment_for_on(self, financial_instrument, date):
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum([open_position.gross_payment_on() for open_position in open_positions if
                    open_position.date() <= date])

    def current_position_for_on(self, financial_instrument, date):
        open_positions = self.open_positions.setdefault(financial_instrument, [])
        return sum([open_position.balance_on(date) for open_position in open_positions])

    def has_or_had_position_for(self, financial_instrument):
        return self.open_positions.get(financial_instrument) is not None


class InvestmentPerformance:
    def __init__(self, financial_instrument, current_position, average_price, total_investment, current_price,
                 price_difference_result, payments_result, sales_result, commissions_result, performance_rate,
                 open_position=None):
        self.financial_instrument = financial_instrument
        self.current_position = current_position
        self.average_price = average_price
        self.total_investment = total_investment
        self.current_price = current_price
        self.valuated_position = round(self.current_position * self.current_price, 2)
        self.price_difference_result = price_difference_result
        self.payments_result = payments_result
        self.sales_result = sales_result
        self.commissions_result = commissions_result
        self.performance_rate = performance_rate
        self.total = round(price_difference_result + payments_result + sales_result + commissions_result, 2)
        self.open_position = open_position


class InvestmentPerformanceCalculator:
    def __init__(self, account, financial_instruments, currency, date, broker=None):
        self.account = account
        self.transaction_manager = TransactionManager(account)
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
                transactions = self.transaction_manager.transactions
            else:
                transactions = [transaction for transaction in self.transaction_manager.transactions if
                                transaction.broker == self.broker]
            self._stock_system = StockSystem(transactions)
        return self._stock_system

    def instrument_performances(self):
        performances = [InvestmentPerformance(financial_instrument, self.current_position_for(financial_instrument),
                                              self.average_price_for(financial_instrument),
                                              self.total_investment_for(financial_instrument),
                                              self.current_price_for(financial_instrument),
                                              self.price_differences_result_for(financial_instrument),
                                              self.payments_result_for(financial_instrument),
                                              self.sales_result_for(financial_instrument),
                                              self.commissions_result_for(financial_instrument),
                                              self.performance_rate(financial_instrument)) for
                        financial_instrument in self.financial_instruments if
                        self.stock_system().has_or_had_position_for(financial_instrument)]
        return [performance for performance in performances if
                (performance.current_position != 0 or performance.total != 0)]

    def open_position_performances(self):
        performances = []
        for financial_instrument in self.financial_instruments:
            performances.extend(
                [InvestmentPerformance(financial_instrument, open_position.security_quantity(),
                                       self.round_two_decimals(open_position.price()),
                                       self.round_two_decimals(open_position.gross_payment_on()),
                                       self.current_price_for(financial_instrument),
                                       self.position_price_differences_result(open_position),
                                       self.position_payments_result(open_position),
                                       self.position_sales_result(open_position),
                                       self.position_commissions_result(open_position),
                                       self.position_performance_rate(open_position),
                                       open_position=open_position) for
                 open_position in self.open_positions(financial_instrument) if
                 self.stock_system().has_or_had_position_for(financial_instrument)])
        return [performance for performance in performances if
                (performance.current_position != 0 or performance.total != 0)]

    def open_positions(self, financial_instrument):
        return self.stock_system().open_positions.setdefault(financial_instrument, [])

    def convert_to(self, amount, currency):
        return convert_to(amount, currency, self.date)

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

    def total_investment_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().total_investment_for_on(financial_instrument, self.date))

    def current_price_for(self, financial_instrument):
        return self.round_and_convert_to(
            self.valuation_system.valuate_instrument_on(financial_instrument, self.currency, self.date))

    def price_differences_result_for(self, financial_instrument):
        return self.round_and_convert_to(
            self.stock_system().price_difference_result_for_on_using(financial_instrument, self.currency, self.date,
                                                                     self.valuation_system))

    def position_price_differences_result(self, open_position):
        return self.round_and_convert_to(
            self.stock_system().position_price_difference_result(open_position, self.currency, self.date,
                                                                 self.valuation_system))

    def payments_result_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().payments_result_for_on(financial_instrument, self.date))

    def position_payments_result(self, open_position):
        # TODO: Hacer bien, ponderado?
        return self.round_and_convert_to(0)

    def sales_result_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().sales_result_for_on(financial_instrument, self.date))

    def position_sales_result(self, open_position):
        return self.round_and_convert_to(self.stock_system().position_sales_result(open_position, self.date))

    def commissions_result_for(self, financial_instrument):
        return self.round_and_convert_to(self.stock_system().commissions_result_for_on(financial_instrument, self.date))

    def position_commissions_result(self, open_position):
        return self.round_and_convert_to(self.stock_system().position_commissions_result(open_position, self.date))

    def performance_rate(self, financial_instrument):
        return self.stock_system().performance_rate(financial_instrument, self.currency, self.date,
                                                    self.valuation_system)

    def position_performance_rate(self, open_position):
        return self.stock_system().position_performance_rate(open_position, self.currency, self.date,
                                                             self.valuation_system)
