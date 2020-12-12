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

    # class Proxy(CompositeField.Proxy):
    #    def __getattr__(self, item):
    #        try:
    #            return super().__getattr__(item)
    #        except AttributeError:

    #    def measurement(self):
    #        return Measurement(getattr(self, 'quantity'), getattr(self, 'unit'))
#
#    def __eq__(self, other):
#        return self.measurement().__eq__(other)
#
#    def __add__(self, other):
#        return self.measurement().__add__(other)
#
#    def __radd__(self, other):
#        return self.measurement().__radd__(other)
#
#    def __sub__(self, other):
#        return self.measurement().__sub__(other)
#
#    def __rsub__(self, other):
#        return self.measurement().__rsub__(other)
#
#    def __mul__(self, other):
#        return self.measurement().__mul__(other)
#
#    def __rmul__(self, other):
#        return self.measurement().__rmul__(other)
#
#    def value(self):
#        return self.measurement().value()
#
