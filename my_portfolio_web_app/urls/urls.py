from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import (
    include,
    path,
)
from django.views.generic import RedirectView

from my_portfolio_web_app.model.financial_instrument import (
    Bond,
    Currency,
    Stock,
)
from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)
from my_portfolio_web_app.views.financial_instrument_views import (
    FinancialInstrumentCreateView,
    FinancialInstrumentDeleteView,
    FinancialInstrumentListView,
    FinancialInstrumentUpdateView,
)
from my_portfolio_web_app.views.import_views import (
    ImportGoogleSheetCashFlowsView,
    ImportGoogleSheetOperationsView,
    ImportIOLOperationsView,
)
from my_portfolio_web_app.views.investment_account_views import (
    AccountPerformanceView,
    FinancialInstrumentPerformanceView,
    InvestmentAccountCreateView,
    InvestmentAccountDeleteView,
    InvestmentAccountListView,
    InvestmentAccountUpdateView,
)
from my_portfolio_web_app.views.views import (
    HomeView,
    MyPortfolioDetailView,
    StockView,
)

app_name = 'my-portfolio'
urlpatterns = [
    path('', HomeView.as_view(), name='index_view'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('my_portfolio/my_portfolio_logo.png'))),
    path('financial-instruments/', FinancialInstrumentListView.as_view(), name='financial_instruments_list'),
    path('financial-instruments/currency/<int:pk>/', MyPortfolioDetailView.as_view(model=Currency),
         name='currency_detail'),
    path('financial-instruments/stock/<int:pk>/', MyPortfolioDetailView.as_view(model=Stock),
         name='stock_detail'),
    path('financial-instruments/bond/<int:pk>/', MyPortfolioDetailView.as_view(model=Bond), name='bond_detail'),
    path('add-financial-instrument/currency/', FinancialInstrumentCreateView.as_view(model=Currency),
         name='currency_create'),
    path('add-financial-instrument/stock/', FinancialInstrumentCreateView.as_view(model=Stock), name='stock_create'),
    path('add-financial-instrument/bond/', FinancialInstrumentCreateView.as_view(model=Bond), name='bond_create'),
    path('edit-financial-instrument/currency/<int:pk>/', FinancialInstrumentUpdateView.as_view(model=Currency),
         name='currency_update'),
    path('edit-financial-instrument/stock/<int:pk>/', FinancialInstrumentUpdateView.as_view(model=Stock),
         name='stock_update'),
    path('edit-financial-instrument/bond/<int:pk>/', FinancialInstrumentUpdateView.as_view(model=Bond),
         name='bond_update'),
    path('delete-financial-instrument/currency/<int:pk>/', FinancialInstrumentDeleteView.as_view(model=Currency),
         name='currency_delete'),
    path('delete-financial-instrument/stock/<int:pk>/', FinancialInstrumentDeleteView.as_view(model=Stock),
         name='stock_delete'),
    path('delete-financial-instrument/bond/<int:pk>/',
         FinancialInstrumentDeleteView.as_view(model=Bond, template_name='my_portfolio/bond_delete_form.html'),
         name='bond_delete'),
    path('accounts/', InvestmentAccountListView.as_view(), name='investment_account_list'),
    path('accounts/account/<int:pk>/', MyPortfolioDetailView.as_view(model=InvestmentIndividualAccount),
         name='account_detail'),
    path('accounts/portfolio/<int:pk>/',
         MyPortfolioDetailView.as_view(model=InvestmentPortfolio, fields=['description', 'individual_accounts']),
         name='portfolio_detail'),
    path('accounts/add/account/', InvestmentAccountCreateView.as_view(model=InvestmentIndividualAccount),
         name='account_create'),
    path('accounts/add/portfolio/',
         InvestmentAccountCreateView.as_view(model=InvestmentPortfolio, fields=['description', 'individual_accounts']),
         name='portfolio_create'),
    path('accounts/edit/account/<int:pk>/', InvestmentAccountUpdateView.as_view(model=InvestmentIndividualAccount),
         name='account_update'),
    path('accounts/edit/portfolio/<int:pk>/',
         InvestmentAccountUpdateView.as_view(model=InvestmentPortfolio, fields=['description', 'individual_accounts']),
         name='portfolio_update'),
    path('accounts/delete/account/<int:pk>/', InvestmentAccountDeleteView.as_view(model=InvestmentIndividualAccount),
         name='account_delete'),
    path('accounts/delete/portfolio/<int:pk>/',
         InvestmentAccountDeleteView.as_view(model=InvestmentPortfolio, fields=['description', 'individual_accounts']),
         name='portfolio_delete'),
    path('stocks/', StockView.as_view(), name='stock_view'),
    path('import/IOL/', ImportIOLOperationsView.as_view(), name='import_iol_operations_view'),
    path('import/operations/google_sheet/', ImportGoogleSheetOperationsView.as_view(),
         name='import_sheet_operations_view'),
    path('import/cash_flows/google_sheet/', ImportGoogleSheetCashFlowsView.as_view(),
         name='import_sheet_cash_flows_view'),
    path('portfolio/<int:pk>/',
         AccountPerformanceView.as_view(model=InvestmentPortfolio),
         name='portfolio_performance_view'),
    path('account/<int:pk>/',
         AccountPerformanceView.as_view(model=InvestmentIndividualAccount),
         name='account_performance_view'),
    path('account/<int:pk>/<int:instrument_pk>/',
         FinancialInstrumentPerformanceView.as_view(model=InvestmentIndividualAccount),
         name='financial_instrument_performance_view'),
    path('transactions/', include('my_portfolio_web_app.urls.transactions_urls'), name='transactions'),
    path('users/', include('django.contrib.auth.urls')),
]
