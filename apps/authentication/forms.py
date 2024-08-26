from django.contrib.auth import forms
from .models import User


class UserCreationForm(forms.UserCreationForm):

    class Meta(forms.UserCreationForm.Meta):
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


class UserChangeForm(forms.UserChangeForm):

    class Meta(forms.UserChangeForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AuthenticationForm(forms.AuthenticationForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "input-field input-default"

        self.fields["password"].widget.attrs["class"] = "input-field input-default"
