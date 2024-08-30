from django.conf import settings
from django.http import HttpResponseRedirect
from functools import wraps


def redirect_authenticated_user(function):

    @wraps(function)
    def inner_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        result = function(request, *args, **kwargs)

        return result

    return inner_function
