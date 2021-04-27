from django.urls import (
    path,
    re_path,
)

from .model.investment_account import (
    InvestmentPortfolio,
    InvestmentIndividualAccount,
)
from .views import (
    index_view,
    AccountPerformanceView,
    StockView,
    ImportIOLOperationsView,
    PurchaseListView,
    TransactionsListView,
    CurrencyDetailView,
    FinancialInstrumentListView,
    StockDetailView,
    BondDetailView,
    StockCreateView,
    StockDeleteView,
)

app_name = 'my-portfolio'
urlpatterns = [
    path('', index_view, name='index_view'),
    path('add-financial-instrument/', StockCreateView.as_view(), name='create_financial_instrument'),
    path('delete-financial-instrument/<int:pk>/', StockDeleteView.as_view(), name='delete_financial_instrument'),
    path('financial-instruments', FinancialInstrumentListView.as_view(), name='financial_instruments_list'),
    path('financial-instruments/currency/<int:pk>/', CurrencyDetailView.as_view(), name='currency_detail'),
    path('financial-instruments/stock/<int:pk>/', StockDetailView.as_view(), name='stock_detail'),
    path('financial-instruments/bond/<int:pk>/', BondDetailView.as_view(), name='bond_detail'),
    path('transactions', TransactionsListView.as_view(), name='transactions_list'),
    path('purchases', PurchaseListView.as_view(), name='purchases_list'),
    path('stocks', StockView.as_view(), name='stock_view'),
    path('import', ImportIOLOperationsView.as_view(), name='import_operations_view'),
    re_path('^portfolio/(?P<pk>\d)/?',
            AccountPerformanceView.as_view(model=InvestmentPortfolio),
            name='portfolio_performance_view'),
    re_path('^account/(?P<pk>\d)/?',
            AccountPerformanceView.as_view(model=InvestmentIndividualAccount),
            name='account_performance_view'),
]
