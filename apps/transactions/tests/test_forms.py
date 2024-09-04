from django.test import TestCase
from apps.transactions.forms import TransactionForm


class TransactionFormTestCase(TestCase):

    def test_form_valid(self):
        form = TransactionForm(
            data={
                "category": "Alimentação",
                "amount": 500,
                "kind": "EX",
            }
        )

        self.assertTrue(form.is_valid())

    def test_amount_max_value_validation(self):
        form = TransactionForm(
            data={
                "category": "Alimentação",
                "amount": 20000,
                "kind": "EX",
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
                "kind": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)
        self.assertIn("kind", form.errors)
        self.assertIn("category", form.errors)
