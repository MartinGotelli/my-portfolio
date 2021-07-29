from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import (
    ProtectedError,
)
from django.forms import Form
from django.forms.utils import ErrorDict
from django.http import (
    HttpResponseRedirect,
)
from django.shortcuts import render
from django.utils.decorators import classonlymethod
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import ModelFormMixin

from my_portfolio_web_app.forms import (
    MyPortfolioFormWrapper,
)
from my_portfolio_web_app.model.stock_system import (
    OpenPositionCreator,
)
from my_portfolio_web_app.model.transaction import (
    Transaction,
)


class LoginRequiredView(View):
    @classonlymethod
    def as_view(cls, **initkwargs):
        return login_required(super().as_view(**initkwargs), login_url='/my-portfolio/users/login')


class HomeView(LoginRequiredView):
    template_name = 'my_portfolio/home_view.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class StockView(ListView, LoginRequiredView):
    template_name = 'my_portfolio/stock_view.html'
    context_object_name = 'open_position_list'

    def get_queryset(self):
        return OpenPositionCreator(Transaction.objects.all()).value_as_list()


class FormWrappingView:
    editable = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MyPortfolioFormWrapper(context['form'], self.editable)
        return context


class MyPortfolioAsFormView:
    def __init__(self, model, fields=None, **kwargs):
        super().__init__(**kwargs)
        self._model = model
        self._fields = fields

    @property
    def fields(self):
        if not self._fields:
            self._fields = []
            for field in self.model._meta.fields:
                if field.name not in ('id', 'polymorphic_ctype'):
                    self._fields.append(field.name)
        return self._fields

    @property
    def model(self):
        return self._model


class MyPortfolioDetailView(MyPortfolioAsFormView, FormWrappingView, ModelFormMixin, DetailView, LoginRequiredView):
    template_name = 'my_portfolio/generic_detail_form.html'
    editable = False


class MyPortfolioCreateView(MyPortfolioAsFormView, FormWrappingView, CreateView, LoginRequiredView):

    def form_invalid(self, form: Form):
        if not self.request.POST.get('send'):
            form._errors = ErrorDict({})

        return super(MyPortfolioCreateView, self).form_invalid(form)

    def form_valid(self, form: Form):
        if not self.request.POST.get('send'):
            # Shouldn't save
            return self.form_invalid(form)
        else:
            return super(MyPortfolioCreateView, self).form_valid(form)


class MyPortfolioUpdateView(MyPortfolioAsFormView, FormWrappingView, UpdateView, LoginRequiredView):
    template_name = 'my_portfolio/generic_update_form.html'


class MyPortfolioDeleteView(MyPortfolioAsFormView, FormWrappingView, ModelFormMixin, DeleteView, LoginRequiredView):
    template_name = 'my_portfolio/generic_delete_form.html'
    editable = False

    def post(self, request, *args, **kwargs):
        try:
            return super(MyPortfolioDeleteView, self).post(request, *args, **kwargs)
        except ProtectedError:
            messages.add_message(request, messages.ERROR, 'This object is referenced by other object in the system')
            return HttpResponseRedirect(self.request.path_info)
