from datetime import date

from django.views import generic

from my_portfolio_web_app.model.financial_instrument import FinancialInstrument, Currency
from my_portfolio_web_app.model.investment_account import InvestmentPortfolio, InvestmentIndividualAccount
from my_portfolio_web_app.model.stock_system import OpenPositionCreator, InvestmentPerformance, \
    InvestmentPerformanceCalculator
from my_portfolio_web_app.model.transaction import Transaction, Purchase
from services.iol_api import IOLAPI


class FinancialInstrumentListView(generic.ListView):
    template_name = 'my_portfolio/financial_instrument_list.html'
    context_object_name = 'financial_instrument_list'

    def get_queryset(self):
        return FinancialInstrument.objects.all()


class TransactionsListView(generic.ListView):
    template_name = 'my_portfolio/transaction_list.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        return Transaction.objects.all()


class PurchaseListView(generic.ListView):
    template_name = 'my_portfolio/purchase_list.html'
    context_object_name = 'purchase_list'

    def get_queryset(self):
        return Purchase.objects.all()


class CurrencyDetailView(generic.DetailView):
    model = Currency
    template_name = 'my_portfolio/currency_detail.html'

    def get_queryset(self):
        return Currency.objects.all()


class StockView(generic.ListView):
    template_name = 'my_portfolio/stock_view.html'
    context_object_name = 'open_position_list'

    def get_queryset(self):
        return OpenPositionCreator(Transaction.objects.all()).value_as_list()


class IndexView(generic.ListView):
    template_name = "my_portfolio/index_view.html"
    context_object_name = "investment_performance_list"

    @staticmethod
    def ars():
        return Currency.objects.get(code='$')

    def get_queryset(self):
        performances = InvestmentPerformanceCalculator(InvestmentIndividualAccount.objects.all()[0],
                                                       FinancialInstrument.objects.all(), self.ars(),
                                                       date.today(), broker="IOL").instrument_performances()
        performances.sort(key=lambda performance: performance.financial_instrument.code)

        return performances


class ImportIOLOperationsView(generic.ListView):
    template_name = "my_portfolio/import_operations.html"
    context_object_name = "draft_operations"

    def get_queryset(self):
        IOLAPI().set_user_and_password("mgotelli", "Kilombo6738")
        operations = IOLAPI().operations_from_to("2021-01-05", "2021-01-05")
        #operations.sort(key=lambda draft: draft.date())

        return operations
# class ResultsView(generic.DetailView):
#    model = Question
#    template_name = 'polls/results.html'
#
#
# def vote(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    try:
#        selected_choice = question.choice_set.get(pk=request.POST['choice'])
#    except (KeyError, Choice.DoesNotExist):
#        # Redisplay the question voting form.
#        return render(request, 'polls/currency_detail.html', {
#            'question': question,
#            'error_message': "You didn't select a choice.",
#        })
#    else:
#        selected_choice.votes += 1
#        selected_choice.save()
#        # Always return an HttpResponseRedirect after successfully dealing
#        # with POST data. This prevents data from being posted twice if a
#        # user hits the Back button.
#        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
