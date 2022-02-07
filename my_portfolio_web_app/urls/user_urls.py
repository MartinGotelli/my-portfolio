from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.urls import (
    include,
    path,
)

from my_portfolio_web_app.model.user_integration_configuration import UserIntegrationConfiguration
from my_portfolio_web_app.views.user_views import (
    UserCreateView,
    UserIntegrationConfigurationCreateView,
    UserIntegrationConfigurationUpdateView,
    create_or_update_user_configuration,
)

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('configuration/', create_or_update_user_configuration, name='user_configuration'),
    path('add/configuration/', UserIntegrationConfigurationCreateView.as_view(model=UserIntegrationConfiguration),
         name='user_configuration_create'),
    path('edit/configuration/', UserIntegrationConfigurationUpdateView.as_view(model=UserIntegrationConfiguration),
         name='user_configuration_update'),
    path('logout/', LogoutView.as_view(next_page='my-portfolio:login'), name='logout'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('create/', UserCreateView.as_view(), name='user_create')
]
