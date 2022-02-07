from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from my_portfolio_web_app.forms import (
    UserCreateForm,
    UserIntegrationConfigurationForm,
    UserIntegrationConfigurationUpdateForm,
)
from my_portfolio_web_app.model.user_integration_configuration import UserIntegrationConfiguration
from my_portfolio_web_app.views.views import (
    FormWrappingView,
    LoginRequiredView,
    UpdateView,
)


def create_or_update_user_configuration(request):
    if UserIntegrationConfiguration.objects.filter(user=request.user):
        return redirect('my-portfolio:user_configuration_update')
    else:
        return redirect('my-portfolio:user_configuration_create')


class UserIntegrationConfigurationCreateView(FormWrappingView, CreateView, LoginRequiredView):
    success_url = reverse_lazy('my-portfolio:index_view')
    form_class = UserIntegrationConfigurationForm
    template_name = 'my_portfolio/generic_update_form.html'

    def get_form(self, form_class=None):
        self.initial = {'user': self.request.user.id}
        return super().get_form(form_class)


class UserIntegrationConfigurationUpdateView(FormWrappingView, UpdateView, LoginRequiredView):
    success_url = reverse_lazy('my-portfolio:index_view')
    form_class = UserIntegrationConfigurationUpdateForm
    template_name = 'my_portfolio/generic_update_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['pk'] = UserIntegrationConfiguration.objects.get(user=request.user).id  # Adding PK dynamically


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'my_portfolio/base_create_form.html'
    success_url = reverse_lazy('my-portfolio:login')
