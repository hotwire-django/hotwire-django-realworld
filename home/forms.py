import unicodedata
from django import forms
from django.contrib.auth import (
    password_validation,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm as AuthAuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize("NFKC", super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "username",
            "placeholder": "Username",
            "class": "form-control form-control-lg",
        }


class UserLoginForm(AuthAuthenticationForm):
    username = UsernameField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control form-control-lg",
                "placeholder": "Password",
            }
        ),
    )


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "Password",
                "class": "form-control form-control-lg",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user