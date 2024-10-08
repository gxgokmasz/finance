from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.common.models import CommonBaseModel


class User(CommonBaseModel, AbstractUser):
    email = models.EmailField(_("endereço de email"), unique=True, validators=[validate_email])

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        ordering = ["-date_joined"]
