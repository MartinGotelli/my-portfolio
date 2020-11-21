from model.measurement import NullUnit, Measurement


class InvestmentAccount:
    def __init__(self, description):
        self.description = description


class InvestmentIndividualAccount(InvestmentAccount):
    def __init__(self, description):
        super().__init__(description)
        self.transactions = []

    def __repr__(self):
        return 'Cuenta ' + self.description

    def add_transaction(self, transaction):
        if self.balance_of_on(transaction.financial_instrument,
                              transaction.date) + transaction.signed_security_quantity() < 0:
            raise Exception('Can not sell on short')
        else:
            self.transactions.append(transaction)

    def balance_of_on(self, financial_instrument, date):
        return sum([transaction.signed_security_quantity() for transaction in
                    self.transactions_of_up_to(financial_instrument, date)])

    def transactions_of_up_to(self, financial_instrument, date):
        return filter(
            lambda transaction: transaction.financial_instrument == financial_instrument and transaction.date <= date,
            self.transactions)

    def balances_on(self, date, broker=None):
        return round(Measurement(0, NullUnit()) +
                     (sum([transaction.movements_on(date) for transaction in self.transactions if
                           (broker is None or transaction.broker == broker) and
                           transaction.date <= date])), 2)

    def registered_transactions(self, broker=None):
        return [transaction for transaction in self.transactions if broker is None or transaction.broker == broker]


class InvestmentPortfolio(InvestmentAccount):
    def __init__(self, description, individual_accounts):
        super().__init__(description)
        self.individual_accounts = individual_accounts

    def __repr__(self):
        return 'Portfolio ' + self.description + '\nCon cuentas: ' + ', '.join(
            [str(account) for account in self.individual_accounts])

    def balance_of_on(self, financial_instrument, date):
        return sum([account.balance_of_on(financial_instrument, date) for account in self.individual_accounts])

    def balances_on(self, date, broker=None):
        return round(sum([account.balances_on(date, broker) for account in self.individual_accounts]), 2)

    def registered_transactions(self, broker=None):
        return [transaction for transactions in
                [account.registered_transactions(broker) for account in self.individual_accounts] for
                transaction in transactions]
