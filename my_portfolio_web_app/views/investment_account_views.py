from datetime import date

from django.views.generic import (
    ListView,
)

from my_portfolio_web_app.model.financial_instrument import (
    Currency,
    FinancialInstrument,
)
from my_portfolio_web_app.model.investment_account import (
    InvestmentIndividualAccount,
    InvestmentPortfolio,
)
from my_portfolio_web_app.model.stock_system import InvestmentPerformanceCalculator
from my_portfolio_web_app.views.views import (
    MyPortfolioCreateView,
    MyPortfolioUpdateView,
    MyPortfolioDeleteView,
)


class InvestmentAccountListView(ListView):
    template_name = 'my_portfolio/investment_account_list.html'
    context_object_name = 'investment_account_list'

    def type(self):
        return self.request.GET.get('type')

    def filter(self, investment_accounts):
        return [account for account in investment_accounts if
                not self.type() or account.class_name() == self.type()]

    def get_queryset(self):
        individual_accounts = list(InvestmentIndividualAccount.objects.all())
        portfolios = list(InvestmentPortfolio.objects.all())
        return self.filter(individual_accounts + portfolios)

    def get_context_data(self, **kwargs):
        context = super(InvestmentAccountListView, self).get_context_data(**kwargs)
        context['types'] = (InvestmentIndividualAccount.class_name, InvestmentPortfolio.class_name)
        return context


class InvestmentAccountCreateView(MyPortfolioCreateView):
    template_name = 'my_portfolio/account_create_form.html'
    success_url = '/my-portfolio/accounts/'


class InvestmentAccountUpdateView(MyPortfolioUpdateView):
    success_url = '/my-portfolio/accounts/'


class InvestmentAccountDeleteView(MyPortfolioDeleteView):
    success_url = '/my-portfolio/accounts/'


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
        broker_string = self.request.GET.get('broker')
        if not broker_string:
            return None
        else:
            return broker_string

    def exclusions(self):
        codes_string = self.request.GET.get('exclude', None)
        if not codes_string:
            return {}
        else:
            codes = codes_string.split(',')
            return set([FinancialInstrument.objects.get(code=code) for code in codes])

    def show_currencies(self):
        return self.request.GET.get('show_currencies', 'True').upper() != 'FALSE'

    def hide_closed(self):
        return self.request.GET.get('hide_closed', 'False').upper() == 'TRUE'

    def filtered_performances(self):
        exclusions = self.exclusions()
        if self.hide_closed() or (not self.show_currencies()) or exclusions:
            self._performances = [performance for performance in self._performances if
                                  (not self.hide_closed() or performance.current_position != 0)
                                  and (self.show_currencies() or not performance.financial_instrument.is_currency())
                                  and (performance.financial_instrument not in exclusions)]

    def performances(self):
        if not self._performances:
            self._performances = InvestmentPerformanceCalculator(
                self.account(),
                FinancialInstrument.objects.all(), self.currency(),
                date.today(),
                broker=self.broker()).instrument_performances()
            self.filtered_performances()
        return self._performances

    def account(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    @staticmethod
    def total_performance(performances):
        return round(sum([performance.total for performance in performances]), 2)

    @staticmethod
    def total_valuated_position(performances):
        return round(sum([performance.valuated_position for performance in performances]), 2)

    @staticmethod
    def total_price_difference_result(performances):
        return round(sum([performance.price_difference_result for performance in performances]), 2)

    def get_context_data(self, **kwargs):
        context = super(AccountPerformanceView, self).get_context_data(**kwargs)
        context['account'] = self.account()
        context['currencies'] = Currency.objects.all()
        performances = self.performances()
        context['total_performance'] = self.total_performance(performances)
        context['total_valuated_position'] = self.total_valuated_position(performances)
        context['total_price_difference_result'] = self.total_price_difference_result(performances)
        return context

    def get_queryset(self):
        performances = self.performances()
        performances.sort(key=lambda performance: performance.financial_instrument.code)
        return performances
