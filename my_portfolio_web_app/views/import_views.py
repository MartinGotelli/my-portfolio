from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView

from my_portfolio_web_app.views.views import (
    GoogleCredentialsRequiredView,
    LoginRequiredView,
)
from services.google_sheet_api import GoogleSheetAPI
from services.iol_api import IOLAPI


class ImportIOLOperationsView(ListView, LoginRequiredView):
    template_name = 'my_portfolio/import_iol_operations.html'
    context_object_name = 'draft_operations'

    def from_date(self):
        return self.request.GET.get('from_date')

    def to_date(self):
        return self.request.GET.get('to_date')

    def get_queryset(self):
        if not self.from_date() or not self.to_date():
            return []
        else:
            operations = IOLAPI(self.request.user).operations_from_to(self.from_date(), self.to_date())
            # operations.sort(key=lambda draft: draft.date())

            return operations


class ImportGoogleSheetOperationsView(GoogleCredentialsRequiredView, ListView, LoginRequiredView):
    template_name = 'my_portfolio/import_sheet_operations.html'
    context_object_name = 'draft_operations'

    def from_date(self):
        return self.request.GET.get('from_date')

    def to_date(self):
        return self.request.GET.get('to_date')

    def without_filter(self):
        return self.request.GET.get('all') == 'True'

    def get_queryset(self):
        if (not self.from_date() or not self.to_date()) and not self.without_filter():
            return []
        else:
            operations = GoogleSheetAPI(self.request).operations_from_to(self.from_date(), self.to_date(), self.without_filter())
            # operations.sort(key=lambda draft: draft.date())

            return operations

    def post(self, request, *args, **kwargs):
        operations = self.get_queryset()
        for operation in operations:
            operation.create()
        return HttpResponseRedirect(reverse('my-portfolio:all_transactions_list'))


class ImportGoogleSheetCashFlowsView(GoogleCredentialsRequiredView, ListView, LoginRequiredView):
    template_name = 'my_portfolio/import_sheet_cash_flows.html'
    context_object_name = 'draft_cash_flows'

    def from_date(self):
        return self.request.GET.get('from_date')

    def to_date(self):
        return self.request.GET.get('to_date')

    def without_filter(self):
        return self.request.GET.get('all') == 'True'

    def get_queryset(self):
        if (not self.from_date() or not self.to_date()) and not self.without_filter():
            return []
        else:
            operations = GoogleSheetAPI(self.request).cash_flows_from_to(self.from_date(), self.to_date(), self.without_filter())

            return operations

    def post(self, request, *args, **kwargs):
        operations = self.get_queryset()
        for operation in operations:
            operation.create()
        return HttpResponseRedirect(reverse('my-portfolio:all_transactions_list'))
