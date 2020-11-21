from model.exceptions import InstanceCreationFailed
from model.measurement import Measurement


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
                          ClosingPosition) and self.outflow == other.outflow and self.security_quantity == other.security_quantity

    def date(self):
        return self.outflow.date

    def quantity_on(self, date):
        if date < self.date() or not self.outflow.financial_instrument.is_alive_on(date):
            return 0
        else:
            return self.quantity()

    def quantity(self):
        return Measurement(self.security_quantity, self.outflow.financial_instrument)


class OpenPosition:
    def __init__(self, inflow, closing_positions=None):
        if closing_positions is None:
            closing_positions = []
        self.inflow = inflow
        self.closing_positions = closing_positions

    def __repr__(self):
        return "Partida de " + self.inflow.financial_instrument.code + " - " + str(self.inflow.security_quantity)

    def __eq__(self, other):
        return isinstance(other,
                          OpenPosition) and self.inflow == other.inflow and self.closing_positions == other.closing_positions

    def date(self):
        return self.inflow.date

    def financial_instrument(self):
        return self.inflow.financial_instrument

    def price(self):
        return self.inflow.price

    def balance_on(self, date):
        return self.inflow.security_quantity_if_alive_on(date) - self.closing_positions_balance_on(date)

    def closing_positions_balance_on(self, date):
        return sum([closing_position.quantity_on(date) for closing_position in self.closing_positions if
                    closing_position.date() <= date])

    def add_closing_position(self, closing_position):
        if self.balance_on(closing_position.date()) >= closing_position.quantity():
            self.closing_positions.append(closing_position)
        else:
            raise InstanceCreationFailed("Cannot add a closing position to this open position")

    def available_quantity_for(self, outflow):
        return min(self.balance_on(outflow.date).value(), outflow.security_quantity)


def add_closing_positions_for_to(outflow, open_positions):
    possible_positions = (open_position for open_position in open_positions if
                          open_position.financial_instrument() == outflow.financial_instrument and
                          outflow.date >= open_position.date())
    remaining_quantity = outflow.security_quantity
    try:
        while remaining_quantity != 0:
            open_position = next(possible_positions)
            affected_quantity = min(open_position.available_quantity_for(outflow), remaining_quantity)
            if affected_quantity > 0:
                open_position.add_closing_position(ClosingPosition(outflow, affected_quantity))
            remaining_quantity -= affected_quantity
    except StopIteration:
        raise InstanceCreationFailed("Cannot sell on short")


class OpenPositionCreator:
    def __init__(self, transactions):
        self.inflows = [transaction for transaction in transactions if
                        transaction.transaction_sign() == 1 and not transaction.financial_instrument.is_currency()]
        self.outflows = [transaction for transaction in transactions if
                         transaction.transaction_sign() == -1 and not transaction.financial_instrument.is_currency()]

    def value(self):
        sorted_open_positions = sorted([OpenPosition(transaction) for transaction in self.inflows],
                                       key=lambda open_position: open_position.date())
        for outflow in self.outflows:
            add_closing_positions_for_to(outflow, sorted_open_positions)

        open_positions_by_instrument = {}
        for open_position in sorted_open_positions:
            open_positions_by_instrument.setdefault(open_position.financial_instrument(), []).append(open_position)

        return open_positions_by_instrument


class StockSystem:
    def __init__(self, transactions=None):
        if transactions is None:
            transactions = []
        self.open_positions = OpenPositionCreator(transactions).value()

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
