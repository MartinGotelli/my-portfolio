import persistence.persistence_manager as manager


class InvestmentAccountPersistenceManager(manager.PersistenceManager):
    def file_name(self):
        return "investment_accounts_db"
