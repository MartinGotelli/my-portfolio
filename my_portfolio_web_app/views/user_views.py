from django.urls import reverse_lazy

from my_portfolio_web_app.forms import UserIntegrationConfigurationUpdateForm
from my_portfolio_web_app.views.views import (
    FormWrappingView,
    LoginRequiredView,
    UpdateView,
)


class UserIntegrationConfigurationUpdateView(FormWrappingView, UpdateView, LoginRequiredView):
    success_url = reverse_lazy('my-portfolio:index_view')
    form_class = UserIntegrationConfigurationUpdateForm
    template_name = 'my_portfolio/generic_update_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['pk'] = request.user.id  # Adding PK dynamically
