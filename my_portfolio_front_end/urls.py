"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import (
    path,
    include,
)
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='my-portfolio:index_view')),
    path('admin/', admin.site.urls),
    path('my-portfolio/', include('my_portfolio_web_app.urls.urls'), name="my-portfolio"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('my_portfolio/my_portfolio_logo.png'))),
]
