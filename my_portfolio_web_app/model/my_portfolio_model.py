from django.db.models import Model
from polymorphic.models import PolymorphicModel


class MyPortfolioPolymorphicModel(PolymorphicModel):
    def __str__(self):
        return self.__repr__()

    class Meta:
        abstract = True


class MyPortfolioModel(Model):
    def __str__(self):
        return self.__repr__()

    class Meta:
        abstract = True
