from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ("category", "type", "amount")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].widget.attrs["class"] = "input-field input-default"

        self.fields["type"].widget.attrs["class"] = "input-field input-default"

        self.fields["amount"].widget.attrs["class"] = "input-field input-default"

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if amount > 15000:
            self.add_error("amount", "Uma transação não pode movimentar mais de 15 mil reais")

        return amount
