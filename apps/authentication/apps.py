from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"

    def ready(self):
        try:
            from . import signals  # noqa
        except ImportError as e:
            raise ImportError(e.msg)
