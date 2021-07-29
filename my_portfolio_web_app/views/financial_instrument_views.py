from django.views.generic import (
    ListView,
)

from my_portfolio_web_app.model.financial_instrument import (
    FinancialInstrument,
)
from my_portfolio_web_app.views.views import (
    LoginRequiredView,
    MyPortfolioCreateView,
    MyPortfolioDeleteView,
    MyPortfolioUpdateView,
)


class FinancialInstrumentListView(ListView, LoginRequiredView):
    template_name = 'my_portfolio/financial_instrument_list.html'
    context_object_name = 'financial_instrument_list'

    def type(self):
        return self.request.GET.get('type')

    def filter(self, financial_instruments):
        return [financial_instrument for financial_instrument in financial_instruments if
                not self.type() or financial_instrument.class_name() == self.type()]

    def get_queryset(self):
        return self.filter(FinancialInstrument.objects.order_by('code'))

    def get_context_data(self, **kwargs):
        context = super(FinancialInstrumentListView, self).get_context_data(**kwargs)
        context['types'] = [cls.class_name() for cls in FinancialInstrument.__subclasses__()]
        return context


class FinancialInstrumentCreateView(MyPortfolioCreateView):
    template_name = "my_portfolio/financial_instrument_create_form.html"
    success_url = '/my-portfolio/financial-instruments'


class FinancialInstrumentUpdateView(MyPortfolioUpdateView):
    success_url = '/my-portfolio/financial-instruments'


class FinancialInstrumentDeleteView(MyPortfolioDeleteView):
    success_url = '/my-portfolio/financial-instruments'
