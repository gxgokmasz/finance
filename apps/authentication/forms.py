from django.contrib.auth import forms as auth_forms
from .models import User


class UserCreationForm(auth_forms.UserCreationForm):

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "input-field input-default"

        self.fields["email"].widget.attrs["class"] = "input-field input-default"

        self.fields["password1"].widget.attrs["class"] = "input-field input-default"
        self.fields["password1"].widget.attrs["required"] = True

        self.fields["password2"].widget.attrs["class"] = "input-field input-default"
        self.fields["password2"].widget.attrs["required"] = True


class UserChangeForm(auth_forms.UserChangeForm):

    class Meta(auth_forms.UserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AuthenticationForm(auth_forms.AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "input-field input-default"

        self.fields["password"].widget.attrs["class"] = "input-field input-default"
