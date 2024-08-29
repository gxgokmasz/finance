from django.db import models
from django.utils.translation import gettext_lazy as _
from core.common.models import CommonModel
from apps.authentication.models import User


class Account(CommonModel):
    user = models.OneToOneField(
        User, models.CASCADE, related_name="account", verbose_name=_("usuário")
    )

    def __str__(self):
        return self.user.username
