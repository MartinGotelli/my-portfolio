from django.views.generic import ListView

from services.google_sheet_api import GoogleSheetAPI
from services.iol_api import IOLAPI


class ImportIOLOperationsView(ListView):
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
            operations = IOLAPI().operations_from_to(self.from_date(), self.to_date())
            # operations.sort(key=lambda draft: draft.date())

            return operations


class ImportGoogleSheetOperationsView(ListView):
    template_name = 'my_portfolio/import_sheet_operations.html'
    context_object_name = 'draft_operations'

    def from_date(self):
        return self.request.GET.get('from_date')

    def to_date(self):
        return self.request.GET.get('to_date')

    def get_queryset(self):
        if not self.from_date() or not self.to_date():
            return []
        else:
            operations = GoogleSheetAPI().operations_from_to(self.from_date(), self.to_date())
            # operations.sort(key=lambda draft: draft.date())

            return operations