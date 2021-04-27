from datetime import date

from django.http import (
    HttpResponse,
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
)

from my_portfolio_web_app.model.financial_instrument import (
    FinancialInstrument,
    Currency,
    Stock,
    Bond,
)
from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.stock_system import (
    OpenPositionCreator,
    InvestmentPerformanceCalculator,
)
from my_portfolio_web_app.model.transaction import (
    Transaction,
    Purchase,
)
from services.iol_api import IOLAPI


def index_view(request):
    return HttpResponse("Welcome to My Portfolio")


class FinancialInstrumentListView(ListView):
    template_name = 'my_portfolio/financial_instrument_list.html'
    context_object_name = 'financial_instrument_list'

    def get_queryset(self):
        return FinancialInstrument.objects.order_by('code')


class TransactionsListView(ListView):
    template_name = 'my_portfolio/transaction_list.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        return InvestmentIndividualAccount.objects.all()[2].transactions.order_by('date')


class PurchaseListView(ListView):
    template_name = 'my_portfolio/purchase_list.html'
    context_object_name = 'purchase_list'

    def get_queryset(self):
        return Purchase.objects.all()


class CurrencyDetailView(DetailView):
    model = Currency
    template_name = 'my_portfolio/currency_detail.html'

    def get_queryset(self):
        return self.model.objects.all()


class StockDetailView(DetailView):
    model = Stock
    template_name = 'my_portfolio/stock_detail.html'

    def get_queryset(self):
        return self.model.objects.all()


class BondDetailView(DetailView):
    model = Bond
    template_name = 'my_portfolio/bond_detail.html'

    def get_queryset(self):
        return self.model.objects.all()


class StockView(ListView):
    template_name = 'my_portfolio/stock_view.html'
    context_object_name = 'open_position_list'

    def get_queryset(self):
        return OpenPositionCreator(Transaction.objects.all()).value_as_list()


class AccountPerformanceView(ListView):
    template_name = "my_portfolio/account_performance_view.html"
    context_object_name = "investment_performance_list"

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self._performances = None

    def currency(self):
        currency_code = self.request.GET.get('currency', '$')
        return Currency.objects.get(code=currency_code)

    def broker(self):
        return self.request.GET.get('broker')

    def performances(self):
        if not self._performances:
            self._performances = InvestmentPerformanceCalculator(
                self.account(),
                FinancialInstrument.objects.all(), self.currency(),
                date.today(),
                broker=self.broker()).instrument_performances()
        return self._performances

    def account(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    @staticmethod
    def total_performance(performances):
        return round(sum([performance.total for performance in performances]), 2)

    @staticmethod
    def total_valuated_position(performances):
        return round(sum([performance.valuated_position for performance in performances]), 2)

    def get_context_data(self, **kwargs):
        context = super(AccountPerformanceView, self).get_context_data(**kwargs)
        context['account'] = self.account()
        performances = self.performances()
        context['total_performance'] = self.total_performance(performances)
        context['total_valuated_position'] = self.total_valuated_position(performances)
        return context

    def get_queryset(self):
        performances = self.performances()
        performances.sort(key=lambda performance: performance.financial_instrument.code)
        return performances


class ImportIOLOperationsView(ListView):
    template_name = "my_portfolio/import_operations.html"
    context_object_name = "draft_operations"

    def get_queryset(self):
        operations = IOLAPI().operations_from_to("2021-01-05", "2021-01-05")
        # operations.sort(key=lambda draft: draft.date())

        return operations


class StockCreateView(CreateView):
    template_name = "my_portfolio/stock_create_form.html"
    model = Stock
    fields = ['code', 'description']
    success_url = '/my-portfolio/financial-instruments'


class StockDeleteView(DeleteView):
    template_name = "my_portfolio/stock_delete_form.html"
    model = Stock
    fields = ['code', 'description']
    success_url = '/my-portfolio/financial-instruments'
