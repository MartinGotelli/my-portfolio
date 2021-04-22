from django.urls import path

from . import views

app_name = 'my-portfolio'
urlpatterns = [
    path('financial-instruments', views.FinancialInstrumentListView.as_view(), name='financial_instruments_list'),
    path('financial-instruments/<int:pk>/', views.CurrencyDetailView.as_view(), name='currency_detail'),
    path('transactions', views.TransactionsListView.as_view(), name='transactions_list'),
    path('purchases', views.PurchaseListView.as_view(), name='purchases_list'),
    path('stocks', views.StockView.as_view(), name='stock_view'),
    path('import', views.ImportIOLOperationsView.as_view(), name='import_operations_view'),
    path('', views.IndexView.as_view(), name='index_view')
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
