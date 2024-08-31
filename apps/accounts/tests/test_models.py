from django.test import TestCase
from apps.accounts.models import Account
from apps.authentication.models import User


class AccountTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="user1", password="password123", email="user1@email.com"
        )

    def test_account_created_on_user_created(self):
        self.assertTrue(Account.objects.filter(user=self.user).exists())

    def test_str_return(self):
        self.assertEqual(self.user.account.__str__(), self.user.username)
