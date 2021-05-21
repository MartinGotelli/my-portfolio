from django.views.generic import (
    ListView,
    TemplateView,
)

from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.transaction import (
    Transaction,
    TRANSACTION_CLASSES_BY_TYPES,
)
from my_portfolio_web_app.views.views import (
    MyPortfolioCreateView,
    MyPortfolioUpdateView,
    MyPortfolioDeleteView,
)


class TransactionsListView(ListView):
    template_name = 'my_portfolio/transaction_list.html'
    context_object_name = 'transaction_list'

    def account(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return None
        else:
            return InvestmentIndividualAccount.objects.get(pk=pk)

    def type(self):
        return self.request.GET.get('type')

    def filter(self, transactions):
        return [transaction for transaction in transactions if
                not self.type() or transaction.type == self.type()]

    def get_queryset(self):
        if not self.account():
            return self.filter(Transaction.objects.order_by('date'))
        else:
            return self.filter(Transaction.objects.filter(account=self.account()).order_by('date'))

    def get_context_data(self, **kwargs):
        context = super(TransactionsListView, self).get_context_data(**kwargs)
        context['types'] = TRANSACTION_CLASSES_BY_TYPES.keys()
        return context


class TransactionCreateView(MyPortfolioCreateView):
    template_name = 'my_portfolio/transaction_create_form.html'
    success_url = '/my-portfolio/transactions/'

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(**kwargs)
        context['type'] = self.model.class_name()
        context['types'] = [{
            'description': item[0],
            'value': item[1].class_name()}
            for item in TRANSACTION_CLASSES_BY_TYPES.items()]

        return context


class TransactionSelectionCreateView(TemplateView):
    template_name = 'my_portfolio/transaction_selection_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionSelectionCreateView, self).get_context_data(**kwargs)
        context['types'] = [{
            'description': item[0],
            'value': item[1].class_name()}
            for item in TRANSACTION_CLASSES_BY_TYPES.items()]

        return context


class TransactionUpdateView(MyPortfolioUpdateView):
    success_url = '/my-portfolio/transactions/'


class TransactionDeleteView(MyPortfolioDeleteView):
    success_url = '/my-portfolio/transactions/'
