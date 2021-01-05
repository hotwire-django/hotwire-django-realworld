from django import forms
from .models import Profile
from home.forms import UserCreationForm
from django.db import models
from django.contrib.auth import (
    password_validation,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class EditProfileForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    password = forms.CharField(
        required=False,
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "New Password",
                "class": "form-control form-control-lg",
            }
        ),
    )

    image = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Image URL",
            }
        ),
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Short bio about you",
            }
        ),
    )

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

    def save(self, user, commit=True):
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        user.profile.image = self.cleaned_data.get("image")
        user.profile.bio = self.cleaned_data.get("bio")
        user.profile.save()
        return user
