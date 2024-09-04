from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Account
from core.common.models import CommonModel


class Transaction(CommonModel):

    class TransactionKinds(models.TextChoices):
        EXPENSE = "EX", _("Despesa")
        REVENUE = "RV", _("Receita")

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
    kind = models.CharField(_("gênero"), max_length=7, choices=TransactionKinds)

    def __str__(self):
        return f"{self.kind} - {self.amount} - {self.category}"
