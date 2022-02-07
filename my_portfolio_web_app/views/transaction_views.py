from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    TemplateView,
)

from my_portfolio_web_app.model.investment_account import InvestmentIndividualAccount
from my_portfolio_web_app.model.transaction import (
    TRANSACTION_CLASSES_BY_TYPES,
    Transaction,
)
from my_portfolio_web_app.views.views import (
    LoginRequiredView,
    MyPortfolioCreateView,
    MyPortfolioDeleteView,
    MyPortfolioUpdateView,
)


def clear_all_transactions(request, account_pk: int):
    account = get_object_or_404(InvestmentIndividualAccount, pk=account_pk)
    for transaction in Transaction.objects.filter(account=account):
        transaction.delete()
    return HttpResponseRedirect(reverse('my-portfolio:transactions_list', args=(account.pk,)))


class TransactionsListView(ListView, LoginRequiredView):
    template_name = 'my_portfolio/transaction_list.html'
    context_object_name = 'transaction_list'
    __accounts = None

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
                self.type_condition_for(transaction)
                and self.account_condition_for(transaction)]

    def type_condition_for(self, transaction):
        return not self.type() or transaction.type == self.type()

    def account_condition_for(self, transaction):
        return transaction.account in self.accounts()

    def accounts(self):
        if not self.__accounts:
            self.__accounts = InvestmentIndividualAccount.by_user(self.request.user)
        return self.__accounts

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
    success_url = '/my-portfolio/transactions/transactions/'

    def get_context_data(self, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(**kwargs)
        context['type'] = self.model.class_name()
        context['types'] = [{
            'description': item[0],
            'value': item[1].class_name()}
            for item in TRANSACTION_CLASSES_BY_TYPES.items()]

        return context


class TransactionSelectionCreateView(TemplateView, LoginRequiredView):
    template_name = 'my_portfolio/transaction_selection_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(TransactionSelectionCreateView, self).get_context_data(**kwargs)
        context['types'] = [{
            'description': item[0],
            'value': item[1].class_name()}
            for item in TRANSACTION_CLASSES_BY_TYPES.items()]

        return context


class TransactionUpdateView(MyPortfolioUpdateView):
    success_url = '/my-portfolio/transactions/transactions/'


class TransactionDeleteView(MyPortfolioDeleteView):
    success_url = '/my-portfolio/transactions/transactions/'
