from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView
from .decorators import redirect_authenticated_user
from .forms import AuthenticationForm, UserCreationForm


@method_decorator(redirect_authenticated_user, "dispatch")
@method_decorator(never_cache, "dispatch")
@method_decorator(sensitive_post_parameters(), "dispatch")
class RegistrationView(FormView):
    form_class = UserCreationForm
    template_name = "pages/authentication/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        self.object = form.save()

        return super().form_valid(form)


@method_decorator(redirect_authenticated_user, "dispatch")
class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm
    template_name = "pages/authentication/login.html"


class LogoutView(auth_views.LogoutView):
    pass
