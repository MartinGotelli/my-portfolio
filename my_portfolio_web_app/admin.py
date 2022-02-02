from django.contrib import admin
from django.contrib.admin import ModelAdmin

from my_portfolio_web_app.forms import UserIntegrationConfigurationForm
from my_portfolio_web_app.model.financial_instrument import (
    Bond,
    Currency,
    Stock,
)
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.transaction import (
    CouponClipping,
    Inflow,
    Outflow,
    Purchase,
    Sale,
    StockDividend,
)
from my_portfolio_web_app.model.user_integration_configuration import UserIntegrationConfiguration

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


class UserIntegrationConfigurationAdmin(ModelAdmin):
    form = UserIntegrationConfigurationForm


admin.site.register(UserIntegrationConfiguration, UserIntegrationConfigurationAdmin)
