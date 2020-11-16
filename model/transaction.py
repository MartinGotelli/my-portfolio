from abc import abstractmethod


class Transaction:
    def __init__(self, date, security_quantity, financial_instrument,
                 broker, commissions=0):
        self.date = date
        self.security_quantity = security_quantity
        self.financial_instrument = financial_instrument
        self.broker = broker
        self.commissions = commissions

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


class Trade(Transaction):
    def __init__(self, date, security_quantity, financial_instrument, price, currency, broker):
        super().__init__(date, security_quantity, financial_instrument, broker)
        self.price = price
        self.currency = currency

    def gross_payment(self):
        return self.signed_security_quantity() * self.price

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
