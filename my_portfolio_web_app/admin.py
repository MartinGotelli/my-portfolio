from django.contrib import admin

from my_portfolio_web_app.model.financial_instrument import Currency, Stock, Bond
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.transaction import Sale, Purchase, Outflow, Inflow, CouponClipping, StockDividend

admin.site.register(Currency)
admin.site.register(Bond)
admin.site.register(Stock)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Inflow)
admin.site.register(Outflow)
admin.site.register(CouponClipping)
admin.site.register(StockDividend)
admin.site.register(InvestmentIndividualAccount)