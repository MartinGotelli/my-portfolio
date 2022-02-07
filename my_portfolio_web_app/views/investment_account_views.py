from datetime import date

from django.urls import reverse_lazy
from django.views.generic import ListView

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
    GoogleCredentialsRequiredView,
    LoginRequiredView,
    MyPortfolioCreateView,
    MyPortfolioDeleteView,
    MyPortfolioUpdateView,
)


class InvestmentAccountListView(ListView, LoginRequiredView):
    template_name = 'my_portfolio/investment_account_list.html'
    context_object_name = 'investment_account_list'

    def type(self):
        return self.request.GET.get('type')

    def filter(self, investment_accounts):
        return [account for account in investment_accounts if
                not self.type() or account.class_name() == self.type()]

    def get_queryset(self):
        individual_accounts = list(InvestmentIndividualAccount.by_user(self.request.user))
        portfolios = list(InvestmentPortfolio.by_user(self.request.user))
        return self.filter(individual_accounts + portfolios)

    def get_context_data(self, **kwargs):
        context = super(InvestmentAccountListView, self).get_context_data(**kwargs)
        context['types'] = (InvestmentIndividualAccount.class_name, InvestmentPortfolio.class_name)
        return context


class InvestmentAccountCreateView(MyPortfolioCreateView):
    template_name = 'my_portfolio/account_create_form.html'
    success_url = reverse_lazy('investment_account_list')


class InvestmentAccountUpdateView(MyPortfolioUpdateView):
    success_url = reverse_lazy('investment_account_list')


class InvestmentAccountDeleteView(MyPortfolioDeleteView):
    success_url = reverse_lazy('investment_account_list')


class AccountPerformanceView(GoogleCredentialsRequiredView, ListView, LoginRequiredView):
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
                self.financial_instruments(),
                self.currency(),
                date.today(),
                broker=self.broker(),
                request=self.request
            ).instrument_performances()
            self.filtered_performances()
        return self._performances

    def financial_instruments(self):
        return FinancialInstrument.objects.all()

    def account(self):
        return self.model.objects.get(pk=self.kwargs['pk'])

    def sum_of_performances(self, method, **kwargs):
        return round(sum([getattr(performance, method) for performance in self.performances()]), 2)

    def total_position(self):
        return self.sum_of_performances('current_position')

    def total_performance(self):
        return self.sum_of_performances('total')

    def total_valuated_position(self):
        return self.sum_of_performances('valuated_position')

    def total_price_difference_result(self):
        return self.sum_of_performances('price_difference_result')

    def total_payments_result(self):
        return self.sum_of_performances('payments_result')

    def total_sales_result(self):
        return self.sum_of_performances('sales_result')

    def total_commissions_result(self):
        return self.sum_of_performances('commissions_result')

    def total_investment(self):
        return self.sum_of_performances('total_investment')

    def total_performance_rate(self):
        total_investment = float(self.total_investment())
        if total_investment:
            return sum(
                [performance.performance_rate * float(performance.total_investment) / total_investment for performance
                 in self.performances()])
        else:
            return total_investment

    def get_context_data(self, **kwargs):
        context = super(AccountPerformanceView, self).get_context_data(**kwargs)
        context['account'] = self.account()
        context['currencies'] = Currency.objects.all()
        context['view'] = self
        return context

    def get_queryset(self):
        performances = self.performances()
        performances.sort(key=lambda performance: performance.financial_instrument.code)
        return performances


class FinancialInstrumentPerformanceView(AccountPerformanceView):
    template_name = "my_portfolio/open_position_performance_view.html"

    def financial_instruments(self):
        return [FinancialInstrument.objects.get(pk=self.kwargs['instrument_pk'])]

    def performances(self):
        if not self._performances:
            self._performances = InvestmentPerformanceCalculator(
                self.account(),
                self.financial_instruments(),
                self.currency(),
                date.today(),
                broker=self.broker(),
                request=self.request
            ).open_position_performances()
            self.filtered_performances()
        return self._performances
