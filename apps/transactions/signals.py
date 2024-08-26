from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Transaction
from .utils import update_account_metrics


@receiver(post_save, sender=Transaction)
def transaction_post_save(instance, sender, created, *args, **kwargs):
    update_account_metrics(instance)


@receiver(post_delete, sender=Transaction)
def transaction_post_delete(instance, sender, *args, **kwargs):
    update_account_metrics(instance, "DELETE")
