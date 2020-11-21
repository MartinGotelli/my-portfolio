from abc import abstractmethod

from model.financial_instrument import ars
from model.measurement import Measurement


class Transaction:
    def __init__(self, date, security_quantity, financial_instrument,
                 broker, commissions=0):
        self.date = date
        self.security_quantity = security_quantity
        self.financial_instrument = financial_instrument
        self.broker = broker
        self.commissions = commissions
        self.price = Measurement(0, ars)

    def __repr__(self):
        return '(' + str(self.date) + ') ' + self.type() + ' de ' + str(self.security_quantity) \
               + ' ' + self.financial_instrument.code + ' a través de ' + self.broker

    def signed_security_quantity(self):
        return self.security_quantity * self.transaction_sign()

    @abstractmethod
    def transaction_sign(self):
        pass

    @abstractmethod
    def type(self):
        pass

    def movements_on(self, date):
        return round(-self.commissions - self.gross_payment() + self.security_quantity_if_alive_on(date), 2)

    def security_quantity_if_alive_on(self, date):
        if self.financial_instrument.is_alive_on(date):
            return Measurement(self.signed_security_quantity(),
                               self.financial_instrument)
        else:
            return 0

    @staticmethod
    def gross_payment():
        return 0


class Trade(Transaction):
    def __init__(self, date, security_quantity, financial_instrument, price, broker, commissions=0):
        super().__init__(date, security_quantity, financial_instrument, broker, commissions)
        self.price = price

    def gross_payment(self):
        return round(self.signed_security_quantity() * self.price, 2)

    def currency(self):
        return self.price.unit

    @abstractmethod
    def transaction_sign(self):
        pass

    @abstractmethod
    def type(self):
        pass


class Purchase(Trade):
    def transaction_sign(self):
        return 1

    def type(self):
        return 'Compra'


class Sale(Trade):
    def transaction_sign(self):
        return -1

    def type(self):
        return 'Venta'


class Inflow(Transaction):
    def transaction_sign(self):
        return 1

    def type(self):
        return 'Ingreso'


class Outflow(Transaction):
    def transaction_sign(self):
        return -1

    def type(self):
        return 'Egreso'


class FinancialInstrumentTenderingPayment(Inflow):
    def __init__(self, date, security_quantity, financial_instrument, referenced_financial_instrument, broker,
                 commissions=0):
        super().__init__(date, security_quantity, financial_instrument, broker, commissions)
        self.referenced_financial_instrument = referenced_financial_instrument

    @abstractmethod
    def type(self): pass


class CouponClipping(FinancialInstrumentTenderingPayment):
    def type(self):
        return 'Pago de Renta y/o Amortización'


class StockDividend(FinancialInstrumentTenderingPayment):
    def type(self):
        return 'Pago de Dividendos'
