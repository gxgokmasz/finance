from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Account
from core.common.models import CommonInfo


TRANSACTION_TYPES = [("Expense", "Despesa"), ("Revenue", "Receita")]


class Transaction(CommonInfo):
    account = models.ForeignKey(
        Account,
        models.CASCADE,
        related_name="transactions",
        verbose_name=_("conta"),
        blank=True,
        null=True,
    )
    category = models.CharField(_("categoria"), max_length=60)
    amount = models.DecimalField(_("quantia"), max_digits=7, decimal_places=2)
    type = models.CharField(_("tipo"), max_length=7, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.category}"
