from django.db.models import Sum
from django.utils import timezone
from django.utils.formats import number_format
from apps.accounts.models import Account


def format_currency(amount):
    return number_format(amount, decimal_pos=2, force_grouping=True)


class TransactionsMetrics:

    def __init__(self, user):
        self.account = Account.objects.prefetch_related("transactions").get(user=user)

        self.account_expense_transactions = self.account.transactions.filter(kind="EX")
        self.account_revenue_transactions = self.account.transactions.filter(kind="RV")

        self.account_expenses_total = (
            self.account_expense_transactions.aggregate(total=Sum("amount"))["total"] or 0
        )
        self.account_revenues_total = (
            self.account_revenue_transactions.aggregate(total=Sum("amount"))["total"] or 0
        )
        self.account_balance = self.account_revenues_total - self.account_expenses_total

    def get_balance_metrics(self):
        return {
            "expenses_total": format_currency(self.account_expenses_total),
            "revenues_total": format_currency(self.account_revenues_total),
            "balance": format_currency(self.account_balance),
        }

    def get_currency_percentages(self):
        total_currency = self.account_expenses_total + self.account_revenues_total

        if total_currency == 0:
            return {
                "revenues_percentage": 0,
                "expenses_percentage": 0,
            }

        revenues_percentage = (self.account_revenues_total / total_currency) * 100
        expenses_percentage = (self.account_expenses_total / total_currency) * 100

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
            expense_transactions = self.account_expense_transactions.filter(
                created_at__date=date.replace("/", "-")
            )
            revenue_transactions = self.account_revenue_transactions.filter(
                created_at__date=date.replace("/", "-")
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
