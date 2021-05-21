from my_portfolio_web_app.model.measurement import (
    Measurement,
    NullUnit,
)
from my_portfolio_web_app.model.transaction import Transaction


class TransactionManager:
    def __init__(self, account):
        self.account = account
        self.transactions = self.initialize_transactions()

    def initialize_transactions(self):
        transactions = []
        for account in self.account.accounts():
            transactions.extend(Transaction.objects.filter(account=account))
        return transactions

    def balances_on(self, date, broker=None):
        return round(Measurement(0, NullUnit()) +
                     (sum([transaction.movements_on(date) for transaction in self.transactions if
                           (broker is None or transaction.broker == broker) and
                           transaction.date <= date])), 2)
