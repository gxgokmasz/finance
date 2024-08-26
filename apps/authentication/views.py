from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from .forms import AuthenticationForm, UserCreationForm


class RegistrationView(FormView):
    form_class = UserCreationForm
    template_name = "pages/authentication/register.html"
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home"))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: UserCreationForm):
        form.save()

        return super().form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "pages/authentication/login.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("home"))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: AuthenticationForm):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class LogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    @method_decorator(login_required(), "dispatch")
    def post(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(reverse_lazy("home"))
