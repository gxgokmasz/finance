from django.db import models
from django.utils.translation import gettext_lazy as _
from core.common.models import CommonInfo
from apps.authentication.models import User


class Account(CommonInfo):
    user = models.OneToOneField(
        User, models.CASCADE, related_name="account", verbose_name=_("usuário")
    )
    expenses_total = models.DecimalField(
        _("despesas totais"), max_digits=9, decimal_places=2, default=0
    )
    revenues_total = models.DecimalField(
        _("receitas totais"), max_digits=9, decimal_places=2, default=0
    )
    balance = models.DecimalField(_("saldo"), max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
