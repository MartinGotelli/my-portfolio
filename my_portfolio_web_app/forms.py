from django.forms import (
    ModelForm,
)

from my_portfolio_web_app.model.financial_instrument import Stock


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['code', 'description']
