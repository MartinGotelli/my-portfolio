from composite_field import CompositeField
from django.db.models import DecimalField, ForeignKey, CASCADE

from my_portfolio_web_app.model.financial_instrument import FinancialInstrument
from my_portfolio_web_app.model.measurement import Measurement, NullUnit


class MeasurementField(CompositeField):
    quantity = DecimalField(decimal_places=8, max_digits=20)
    unit = ForeignKey(FinancialInstrument, on_delete=CASCADE, related_name="measurement_unit")

    def __init__(self, verbose_name=None, blank=False, null=False, default=None):
        super(MeasurementField, self).__init__()
        self.verbose_name = verbose_name
        for field in (self['quantity'], self['unit']):
            field.blank = blank
            field.null = null
        if default is not None:
            self['unit'].default = default.unit
            self['quantity'].default = default.quantity

    def contribute_to_class(self, cls, field_name):
        if self.verbose_name is None:
            self.verbose_name = field_name.replace('_', ' ')
        self['quantity'].verbose_name = 'Re(%s)' % self.verbose_name
        self['unit'].verbose_name = 'Im(%s)' % self.verbose_name
        super(MeasurementField, self).contribute_to_class(cls, field_name)

    def get(self, model):
        proxy = self.get_proxy(model)
        quantity, unit = proxy.quantity, proxy.unit
        if quantity is None and unit is None:
            return 0
        return Measurement(quantity or 0, unit or NullUnit())

    def set(self, model, value):
        proxy = self.get_proxy(model)
        if value is None:
            proxy.quantity = None
            proxy.unit = None
        else:
            proxy.quantity = value.quantity
            proxy.unit = value.unit
#
