from django.urls import reverse_lazy

from my_portfolio_web_app.views.views import MyPortfolioUpdateView


class UserIntegrationConfigurationUpdateView(MyPortfolioUpdateView):
    success_url = reverse_lazy('index_view')

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['pk'] = request.user.id  # Adding PK dynamically
