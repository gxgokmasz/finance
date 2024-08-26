from django.db.models import Sum
from django.utils import timezone
from django.utils.formats import number_format
from apps.accounts.models import Account


class TransactionsMetrics:

    def __init__(self, user):
        self.account = Account.objects.get(user=user)

    def format_currency(self, amount):
        return number_format(amount, decimal_pos=2, force_grouping=True)

    def get_profit_metrics(self):
        return {
            "expenses_total": self.format_currency(self.account.expenses_total),
            "revenues_total": self.format_currency(self.account.revenues_total),
            "profit_total": self.format_currency(self.account.balance),
        }

    def get_currency_percentages(self):
        total_currency = self.account.expenses_total + self.account.revenues_total

        if total_currency == 0:
            return {
                "revenues_percentage": 0,
                "expenses_percentage": 0,
            }

        revenues_percentage = (self.account.revenues_total / total_currency) * 100
        expenses_percentage = (self.account.expenses_total / total_currency) * 100

        return {
            "revenues_percentage": f"{revenues_percentage:.2f}",
            "expenses_percentage": f"{expenses_percentage:.2f}",
        }

    def get_weekly_xip_relationship(self):
        today = timezone.now().date().today()
        dates = [
            (today - timezone.timedelta(days=i)).strftime("%Y/%m/%d") for i in range(6, -1, -1)
        ]

        metrics = []

        for date in dates:
            expense_transactions = self.account.transactions.filter(
                type="Expense", created_at__date=date.replace("/", "-")
            )
            revenue_transactions = self.account.transactions.filter(
                type="Revenue", created_at__date=date.replace("/", "-")
            )

            expenses_total = expense_transactions.aggregate(total=Sum("amount"))["total"] or 0
            revenues_total = revenue_transactions.aggregate(total=Sum("amount"))["total"] or 0

            metrics.append(
                {
                    "revenues_total": revenues_total,
                    "expenses_total": expenses_total,
                    "balance": revenues_total - expenses_total,
                }
            )

        return {
            "dates": dates,
            "metrics": metrics,
        }
