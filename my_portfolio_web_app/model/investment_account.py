from django.db.models import CharField, ManyToManyField

from my_portfolio_web_app.model.measurement import NullUnit, Measurement
from my_portfolio_web_app.model.my_portfolio_model import MyPortfolioModel
from my_portfolio_web_app.model.transaction import Transaction


class InvestmentIndividualAccount(MyPortfolioModel):
    description = CharField(max_length=200)
    transactions = ManyToManyField(Transaction)

    def __repr__(self):
        return 'Cuenta ' + self.description

    def add_transaction(self, transaction):
        if self.balance_of_on(transaction.financial_instrument,
                              transaction.date) + transaction.signed_security_quantity() < 0:
            raise Exception('Can not sell on short')
        else:
            self.transactions.add(transaction)

    def balance_of_on(self, financial_instrument, date):
        return float(sum([transaction.signed_security_quantity() for transaction in
                          self.transactions_of_up_to(financial_instrument, date)]))

    def transactions_of_up_to(self, financial_instrument, date):
        return filter(
            lambda transaction: transaction.financial_instrument == financial_instrument and transaction.date <= date,
            self.registered_transactions())

    def balances_on(self, date, broker=None):
        return round(Measurement(0, NullUnit()) +
                     (sum([transaction.movements_on(date) for transaction in self.registered_transactions() if
                           (broker is None or transaction.broker == broker) and
                           transaction.date <= date])), 2)

    def registered_transactions(self, broker=None):
        return [transaction for transaction in self.transactions.all() if
                broker is None or transaction.broker == broker]


class InvestmentPortfolio(MyPortfolioModel):
    description = CharField(max_length=200)
    individual_accounts = ManyToManyField(InvestmentIndividualAccount)

    def __repr__(self):
        return 'Portfolio ' + self.description + '\nCon cuentas: '  # + ', '.join(
        # [str(account) for account in self.individual_accounts.all()])

    def balance_of_on(self, financial_instrument, date):
        return sum([account.balance_of_on(financial_instrument, date) for account in self.individual_accounts.all()])

    def balances_on(self, date, broker=None):
        return round(sum([account.balances_on(date, broker) for account in self.individual_accounts.all()]), 2)

    def registered_transactions(self, broker=None):
        return [transaction for transactions in
                [account.registered_transactions(broker) for account in self.individual_accounts.all()] for
                transaction in transactions]
