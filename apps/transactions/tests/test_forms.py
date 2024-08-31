from django.core.exceptions import ValidationError
from django.test import TestCase
from apps.transactions.forms import TransactionForm
from apps.transactions.models import Transaction


class TransactionFormTestCase(TestCase):

    def test_form_valid(self):
        form = TransactionForm(
            data={
                "category": "Alimentação",
                "amount": 500,
                "genre": "EX",
            }
        )

        self.assertTrue(form.is_valid())

    def test_amount_max_value_validation(self):
        form = TransactionForm(
            data={
                "category": "Alimentação",
                "amount": 20000,
                "genre": "EX",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)
        self.assertEqual(
            form.errors["amount"], ["Uma transação não pode movimentar mais de 15 mil reais"]
        )

    def test_form_empty_fields(self):
        form = TransactionForm(
            data={
                "category": "",
                "amount": "",
                "genre": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)
        self.assertIn("genre", form.errors)
        self.assertIn("category", form.errors)
