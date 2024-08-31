from django.test import TestCase
from apps.authentication.models import User
from apps.transactions.models import Transaction


class TransactionTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="user1", password="password123", email="user1@email.com"
        )

    def test_create_transactions(self):
        transaction = Transaction.objects.create(
            account=self.user.account,
            category="Alimentação",
            amount=500,
            genre="EX",
        )

        self.assertTrue(Transaction.objects.filter(account=self.user.account))
        self.assertEqual(transaction.account, self.user.account)

    def test_str_return(self):
        transaction = Transaction.objects.create(
            account=self.user.account,
            category="Salário",
            amount=5000,
            genre="RV",
        )

        self.assertEqual(
            transaction.__str__(),
            f"{transaction.genre} - {transaction.amount} - {transaction.category}",
        )
