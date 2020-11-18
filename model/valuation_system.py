from model.exceptions import ObjectNotFound


class ValuationSourceFromDictionary:
    def __init__(self, prices):
        self.prices = prices

    def prices_for_on(self, instrument, date):
        return self.prices.setdefault(date, {}).setdefault(instrument, [])

    def add_price_for_on(self, instrument, date, price):
        self.remove_if_exist_price_for_on(instrument, date, price.unit)
        self.prices_for_on(instrument, date).append(price)

    def remove_if_exist_price_for_on(self, instrument, date, currency):
        try:
            price_to_remove = self.price_for_on(instrument, currency, date)
            self.prices_for_on(instrument, date).remove(price_to_remove)
        except ObjectNotFound:
            pass

    def price_for_on(self, instrument, currency, date):
        try:
            return next(filter(lambda price: price.unit == currency,
                               self.prices_for_on(instrument, date)))
        except StopIteration:
            raise ObjectNotFound(
                "There is no " + currency.description + "price for " + instrument.code + " on " + str(date))
