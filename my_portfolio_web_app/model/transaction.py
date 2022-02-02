from abc import abstractmethod

from django.db.models import (
    CharField,
    DecimalField,
    ForeignKey,
    PROTECT,
)

from my_portfolio_web_app.model.financial_instrument import (
    Currency,
    FinancialInstrument,
    ars,
    usd,
)
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.measurement import (
    Measurement,
    NullUnit,
    _round,
    measurements_from,
)
from my_portfolio_web_app.model.my_portfolio_model import (
    CalendarDateField,
    MyPortfolioPolymorphicModel,
)

PURCHASE = 'Compra'
SALE = 'Venta'
INFLOW = 'Ingreso'
OUTFLOW = 'Egreso'
COUPON_CLIPPING = 'Pago de Renta y/o Amortización'
STOCK_DIVIDEND = 'Pago de Dividendos'

BROKERS = [
    ('IOL', 'IOL'),
    ('BALANZ', 'BALANZ'),
]


def amount_for_in(currency, measurement_or_bag):
    measurements = [measurement for measurement in measurements_from(measurement_or_bag) if
                    measurement.unit == currency]
    if not measurements:
        return 0
    else:
        return measurements[0].quantity


class Transaction(MyPortfolioPolymorphicModel):
    date = CalendarDateField('Fecha')
    security_quantity = DecimalField(verbose_name='Cantidad Nominal', decimal_places=2, max_digits=20)
    financial_instrument = ForeignKey(FinancialInstrument, verbose_name='Instrumento', on_delete=PROTECT)
    broker = CharField(max_length=10, choices=BROKERS)
    ars_commissions = DecimalField(verbose_name='Comisiones ($)', decimal_places=2, default=0, max_digits=20)
    usd_commissions = DecimalField(verbose_name='Comisiones (USD)', decimal_places=2, default=0, max_digits=20)
    price_unit = ForeignKey(Currency, on_delete=PROTECT, related_name='price_unit', null=True, blank=True,
                            verbose_name='Moneda de Pago')
    price_amount = DecimalField(decimal_places=6, max_digits=20, default=0.0, verbose_name='Precio')
    account = ForeignKey(InvestmentIndividualAccount, on_delete=PROTECT, verbose_name='Cuenta')

    def __init__(self, *args, **kwargs):
        if 'price' in kwargs:
            price = kwargs.pop('price', None)
            kwargs['price_unit'] = price.unit
            kwargs['price_amount'] = price.value()
        if 'commissions' in kwargs:
            commissions = kwargs.pop('commissions', None)
            kwargs['ars_commissions'] = amount_for_in(ars, commissions)
            kwargs['usd_commissions'] = amount_for_in(usd, commissions)
        super(Transaction, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '(' + str(self.date) + ') ' + self.type + ' de ' + str(self.security_quantity) \
               + ' ' + self.financial_instrument.code + ' a través de ' + self.broker

    def signed_security_quantity(self):
        return self.security_quantity * self.transaction_sign()

    @abstractmethod
    def transaction_sign(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    def movements_on(self, date):
        return _round(-self.commissions() - self.gross_payment() + self.security_quantity_if_alive_on(date), 2)

    def monetary_movements_on(self, date):
        return sum([measurement for measurement in self.movements_on(date).as_bag().non_zero_measurements() if
                    measurement.unit.is_currency()]) + Measurement(0, NullUnit())

    def movements(self):
        return self.movements_on(self.date)

    def monetary_movements(self):
        return self.monetary_movements_on(self.date)

    def security_quantity_if_alive_on(self, date):
        if self.financial_instrument.is_alive_on(date):
            return Measurement(self.signed_security_quantity(),
                               self.financial_instrument)
        else:
            return Measurement(0, NullUnit())

    @staticmethod
    def gross_payment():
        return Measurement(0, NullUnit())

    @staticmethod
    def is_payment():
        return False

    def commissions(self):
        return Measurement(self.ars_commissions, ars) + Measurement(self.usd_commissions, usd)

    def price_unit_or_null(self):
        return self.price_unit or NullUnit()

    def price(self):
        return Measurement(self.price_amount, self.price_unit_or_null())


class Trade(Transaction, MyPortfolioPolymorphicModel):
    def gross_payment(self):
        return _round(self.signed_security_quantity() * self.price(), 2)

    def currency(self):
        return self.price().unit

    @abstractmethod
    def transaction_sign(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass


class Purchase(Trade):
    def transaction_sign(self):
        return 1

    @property
    def type(self):
        return PURCHASE


class Sale(Trade):
    def transaction_sign(self):
        return -1

    @property
    def type(self):
        return SALE


class Inflow(Transaction):
    def transaction_sign(self):
        return 1

    @property
    def type(self):
        return INFLOW


class Outflow(Transaction):
    def transaction_sign(self):
        return -1

    @property
    def type(self):
        return OUTFLOW


class FinancialInstrumentTenderingPayment(Transaction, MyPortfolioPolymorphicModel):
    referenced_financial_instrument = ForeignKey(FinancialInstrument, on_delete=PROTECT,
                                                 verbose_name='Instrumento Referencia')

    @abstractmethod
    def type(self): pass

    @staticmethod
    def is_payment():
        return True

    def transaction_sign(self):
        return 1

    def gross_payment(self):
        return Measurement(self.signed_security_quantity(), self.financial_instrument)

    def movements_on(self, date):
        return _round(-self.commissions() + self.gross_payment(), 2)


class CouponClipping(FinancialInstrumentTenderingPayment):
    @property
    def type(self):
        return COUPON_CLIPPING


class StockDividend(FinancialInstrumentTenderingPayment):
    @property
    def type(self):
        return STOCK_DIVIDEND


TRANSACTION_CLASSES_BY_TYPES = {
    PURCHASE: Purchase,
    SALE: Sale,
    INFLOW: Inflow,
    OUTFLOW: Outflow,
    COUPON_CLIPPING: CouponClipping,
    STOCK_DIVIDEND: StockDividend,
}
