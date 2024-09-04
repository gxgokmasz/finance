import pandas as pd
from django.core.management.base import BaseCommand
from apps.authentication.models import User
from apps.transactions.models import Transaction


class Command(BaseCommand):

    def add_arguments(self, parser) -> None:
        parser.add_argument("user")

    def handle(self, *args, **options):
        try:
            transactions_df = pd.read_csv("mocks/transactions.csv", encoding="UTF-8")

            for _, row in transactions_df.iterrows():
                kind = row["kind"]
                category = row["category"]
                amount = row["amount"]

                try:
                    user = User.objects.get(username=options["user"])
                except User.DoesNotExist as e:
                    raise User.DoesNotExist(e)

                new_transaction = Transaction.objects.create(
                    account=user.account, kind=kind, category=category, amount=amount
                )

                notice_text = "%s - %d - %s" % (
                    new_transaction.kind,
                    new_transaction.amount,
                    new_transaction.category,
                )

                self.stdout.write(self.style.NOTICE(notice_text))

            self.stdout.write(self.style.SUCCESS("TRANSAÇÕES IMPORTADAS COM SUCESSO!"))
        except pd.errors.ParserError as exc:
            self.stderr.write(self.style.ERROR(f"Erro ao processar o arquivo CSV: {exc}"))
