from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import (
    CharField,
    EmailField,
    HiddenInput,
    ModelForm,
    PasswordInput,
)

from my_portfolio_web_app.model.user_integration_configuration import UserIntegrationConfiguration


class MyPortfolioFormWrapper:
    def __init__(self, form, editable=True):
        self.form = form
        self.editable = editable
        if not self.editable:
            for field in self.form.fields.values():
                field.widget.attrs['disabled'] = True

    def __getattr__(self, name):
        if name in ('as_table', 'form'):
            return super().__getattr__
        else:
            return self.form.__getattr__

    def as_table(self):
        return self.form._html_output(
            normal_row='<tr%(html_class_attr)s><th>%(label)s</th><td>%(field)s%(help_text)s</td></tr>',
            error_row='<tr><td colspan="2">%s</td></tr>',
            row_ender='</td></tr>',
            help_text_html='<br><span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )

    def as_hidden(self):
        original_fields = self.form.fields.copy()
        for field in self.form.fields.values():
            field.widget = HiddenInput(field.widget.attrs)

        output = self.form._html_output(
            normal_row='%(field)s',
            error_row='',
            row_ender='',
            help_text_html='',
            errors_on_separate_row=False,
        )

        self.form.fields = original_fields

        return output


class UserIntegrationConfigurationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled = True

    class Meta:
        model = UserIntegrationConfiguration
        fields = ['user', 'iol_username', 'iol_password', 'google_sheet_id']
        widgets = {
            'iol_password': PasswordInput(),
        }


class UserIntegrationConfigurationUpdateForm(ModelForm):
    class Meta:
        model = UserIntegrationConfiguration
        fields = ['iol_username', 'iol_password', 'google_sheet_id']
        widgets = {
            'iol_password': PasswordInput(),
        }


class UserCreateForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden',
    }
    password1 = CharField(
        label="Contraseña",
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=False,
    )
    password2 = CharField(
        label="Repetir Contraseña",
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=False,
    )
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {k: '' for k in fields}
