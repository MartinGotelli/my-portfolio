from django.urls import path

from my_portfolio_web_app.model.transaction import (
    Purchase,
    StockDividend,
    CouponClipping,
    Outflow,
    Inflow,
    Sale,
)
from my_portfolio_web_app.views.transaction_views import (
    TransactionsListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionSelectionCreateView,
    clear_all_transactions,
)

urlpatterns = [
    path('transactions/<int:pk>/', TransactionsListView.as_view(), name='transactions_list'),
    path('transactions/', TransactionsListView.as_view(), name='all_transactions_list'),
    path('transactions/clear/<int:account_pk>', clear_all_transactions, name='clear_transactions'),
    path('transactions/add/', TransactionSelectionCreateView.as_view(), name='transaction_create'),
    path('transactions/add/purchase/', TransactionCreateView.as_view(model=Purchase), name='purchase_create'),
    path('transactions/add/sale/', TransactionCreateView.as_view(model=Sale), name='sale_create'),
    path('transactions/add/inflow/', TransactionCreateView.as_view(model=Inflow), name='inflow_create'),
    path('transactions/add/outflow/', TransactionCreateView.as_view(model=Outflow), name='outflow_create'),
    path('transactions/add/coupon_clipping/', TransactionCreateView.as_view(model=CouponClipping),
         name='coupon_clipping_create'),
    path('transactions/add/stock_dividend/', TransactionCreateView.as_view(model=StockDividend),
         name='stock_dividend_create'),
    path('transactions/edit/purchase/<int:pk>/', TransactionUpdateView.as_view(model=Purchase), name='purchase_update'),
    path('transactions/edit/sale/<int:pk>/', TransactionUpdateView.as_view(model=Sale), name='sale_update'),
    path('transactions/edit/inflow/<int:pk>/', TransactionUpdateView.as_view(model=Inflow), name='inflow_update'),
    path('transactions/edit/outflow/<int:pk>/', TransactionUpdateView.as_view(model=Outflow), name='outflow_update'),
    path('transactions/edit/coupon_clipping/<int:pk>/', TransactionUpdateView.as_view(model=CouponClipping),
         name='coupon_clipping_update'),
    path('transactions/edit/stock_dividend/<int:pk>/', TransactionUpdateView.as_view(model=StockDividend),
         name='stock_dividend_update'),
    path('transactions/delete/purchase/<int:pk>/', TransactionUpdateView.as_view(model=Purchase),
         name='purchase_delete'),
    path('transactions/delete/sale/<int:pk>/', TransactionUpdateView.as_view(model=Sale), name='sale_delete'),
    path('transactions/delete/inflow/<int:pk>/', TransactionUpdateView.as_view(model=Inflow), name='inflow_delete'),
    path('transactions/delete/outflow/<int:pk>/', TransactionUpdateView.as_view(model=Outflow), name='outflow_delete'),
    path('transactions/delete/coupon_clipping/<int:pk>/', TransactionUpdateView.as_view(model=CouponClipping),
         name='coupon_clipping_delete'),
    path('transactions/delete/stock_dividend/<int:pk>/', TransactionUpdateView.as_view(model=StockDividend),
         name='stock_dividend_delete'),
]
