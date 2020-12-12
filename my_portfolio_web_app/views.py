from django.views import generic

from my_portfolio_web_app.model.financial_instrument import FinancialInstrument, Currency
from my_portfolio_web_app.model.transaction import Transaction, Purchase


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
