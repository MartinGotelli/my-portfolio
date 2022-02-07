from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
)
from django_cryptography.fields import encrypt


from my_portfolio_web_app.model.my_portfolio_model import MyPortfolioModel


class UserIntegrationConfiguration(MyPortfolioModel):
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='Usuario')
    iol_username = CharField(max_length=200, verbose_name='Usuario IOL')
    iol_password = encrypt(CharField(max_length=200, verbose_name='Contraseña IOL'))
    google_sheet_id = CharField(max_length=255, verbose_name='ID Google Sheet')

    def __repr__(self):
        return f'Configuración para {self.user}'
