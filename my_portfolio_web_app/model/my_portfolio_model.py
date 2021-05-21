import re

from django.db.models import (
    Model,
    CharField,
    DateField,
)
from django.forms import (
    TextInput,
    DateInput,
)
from polymorphic.models import PolymorphicModel


class MyPortfolioModelBehavior:
    def class_name(self):
        return self.__class__.class_name()

    @classmethod
    def class_name(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()


class MyPortfolioPolymorphicModel(PolymorphicModel, MyPortfolioModelBehavior):
    def __str__(self):
        return self.__repr__()

    class Meta:
        abstract = True


class MyPortfolioModel(Model, MyPortfolioModelBehavior):
    def __str__(self):
        return self.__repr__()

    class Meta:
        abstract = True


class UpperCaseCharField(CharField):

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.upper()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(UpperCaseCharField, self).pre_save(model_instance, add)

    def formfield(self, **kwargs):
        defaults = {'widget': TextInput(attrs={'style': 'text-transform:uppercase;'})}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class CalendarDateInput(DateInput):
    input_type = 'date'


class CalendarDateField(DateField):
    def formfield(self, **kwargs):
        defaults = {'widget': CalendarDateInput()}
        defaults.update(kwargs)
        return super().formfield(**defaults)
