from collections import defaultdict

from my_portfolio_web_app.model.measurement import (
    Measurement,
    NullUnit,
)
from my_portfolio_web_app.model.transaction import Transaction


class TransactionManager:
    def __init__(self, account):
        self.account = account
        self.transactions = self.initialize_transactions()
        self.balances = defaultdict(lambda: defaultdict(list))

    def initialize_transactions(self):
        transactions = []
        for account in self.account.accounts():
            transactions.extend(Transaction.objects.filter(account=account))
        return transactions

    def registered_transactions(self, broker=None):
        if broker:
            return [transaction for transaction in self.transactions if transaction.broker == broker]
        else:
            return self.transactions

    def balance_of_on(self, financial_instrument, date, broker=None):
        return float(sum(filter(lambda balance: balance.unit == financial_instrument, self.balances_on(date, broker))))

    def balances_on(self, date, broker=None):
        if not self.balances[date][broker]:
            self.balances[date][broker] = round(Measurement(0, NullUnit()) +
                                                (sum(
                                                    [transaction.movements_on(date) for transaction in
                                                     self.registered_transactions(broker) if
                                                     transaction.date <= date])), 2)
        return self.balances[date][broker]
