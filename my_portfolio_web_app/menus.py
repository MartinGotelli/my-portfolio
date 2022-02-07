from django.shortcuts import redirect

from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)


class MenuBehavior:
    def __init__(self, view_name, title, prefix='my-portfolio:', menu_items=None, arguments=None):
        if view_name is None:
            self.view_name = None
        else:
            self.view_name = prefix + view_name
        self.title = title
        if menu_items is None:
            menu_items = []
        self.items = menu_items
        if arguments is None:
            arguments = {}
        self.arguments = arguments

    @property
    def url(self):
        return redirect(self.view_name, **self.arguments).url


class ClickableMenu(MenuBehavior):
    def __init__(self, view_name, title, prefix='my-portfolio:', menu_items=None, arguments=None):
        super(ClickableMenu, self).__init__(view_name=view_name, title=title, prefix=prefix, menu_items=menu_items,
                                            arguments=arguments)


class NonClickableMenu(MenuBehavior):
    def __init__(self, title, menu_items=None, arguments=None):
        super(NonClickableMenu, self).__init__(view_name=None, title=title, menu_items=menu_items, arguments=arguments)

    @property
    def html(self):
        title = f'<div class="dropdown-submenu"><a>{self.title}</a>'
        submenus = f'<div class="subdropdown-content">{"".join([item.html for item in self.items])}</div></div>'
        return title + '\n' + submenus


class MenuItem(MenuBehavior):
    def __init__(self, view_name, title, prefix='my-portfolio:', arguments=None):
        super(MenuItem, self).__init__(view_name=view_name, title=title, prefix=prefix, arguments=arguments)

    @property
    def html(self):
        return f'<a href={self.url}>{self.title}</a>'


class Separator:
    @property
    def html(self):
        return '<div class="dropdown-divider"></div>'


def account_sub_items(view_name, user):
    return [
        MenuItem(view_name, account.description, arguments={'pk': account.pk}) for account in
        InvestmentIndividualAccount.by_user(user)
    ]


def portfolio_sub_items(view_name, user):
    return [
        MenuItem(view_name, portfolio.description, arguments={'pk': portfolio.pk}) for portfolio in
        InvestmentPortfolio.by_user(user)
    ]


def menu_items(request):
    separator = [Separator()]
    return {
        'menu_items': [
            MenuItem('index_view', 'Home'),
            ClickableMenu('financial_instruments_list', 'Instrumentos', menu_items=[
                MenuItem('stock_create', 'Agregar Acción'),
                MenuItem('currency_create', 'Agregar Moneda'),
                MenuItem('bond_create', 'Agregar Bono'),
            ]),
            ClickableMenu('investment_account_list', 'Cuentas', menu_items=[
                MenuItem('account_create', 'Agregar Cuenta'),
                MenuItem('portfolio_create', 'Agregar Portfolio'),
            ]),
            NonClickableMenu('Resultados',
                             menu_items=account_sub_items('account_performance_view', request.user) +
                                        separator +
                                        portfolio_sub_items('portfolio_performance_view', request.user)
                             ),
            ClickableMenu('all_transactions_list', 'Transacciones',
                          menu_items=account_sub_items('transactions_list', request.user) + separator + [
                              MenuItem('transaction_create', 'Agregar')]),
            MenuItem('stock_view', 'Partidas'),
            NonClickableMenu('Importar', menu_items=[
                MenuItem('import_iol_operations_view', 'InvertirOnline'),
                NonClickableMenu('Google Sheet', menu_items=[
                    MenuItem('import_sheet_operations_view', 'Operaciones'),
                    MenuItem('import_sheet_cash_flows_view', 'Ingresos/Egresos'),
                ]),
                # MenuItem('import_sheet_operations_view', 'Operaciones'),
                # MenuItem('import_sheet_cash_flows_view', 'Ingresos/Egresos'),
            ]),
        ]}
