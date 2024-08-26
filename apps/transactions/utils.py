from decimal import Decimal


def update_account_metrics(instance, action_type=None):
    amount = Decimal(instance.amount)
    account = instance.account
    amount_by_action = -amount if action_type == "DELETE" else amount

    if instance.type == "Expense":
        account.expenses_total += amount_by_action
        account.balance -= amount_by_action
    elif instance.type == "Revenue":
        account.revenues_total += amount_by_action
        account.balance += amount_by_action

    account.save()
