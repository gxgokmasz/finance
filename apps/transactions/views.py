from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import TransactionForm
from .metrics import TransactionsMetrics
from .models import Transaction


@method_decorator(login_required(), "dispatch")
class TransactionListView(ListView):
    model = Transaction
    template_name = "pages/transactions/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 8

    def initialize_requests_common_data(self, request, *args, **kwargs):
        transactions_metrics = TransactionsMetrics(request.user)

        self.balance_metrics = transactions_metrics.get_balance_metrics()

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.initialize_requests_common_data(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        transactions = super().get_queryset()

        request_account_transactions = transactions.filter(account=self.request.user.account)

        transaction_search = self.request.GET.get("transaction_search")

        if transaction_search:
            transactions_filtered_by_category = request_account_transactions.filter(
                category__icontains=transaction_search
            )

            return transactions_filtered_by_category

        return request_account_transactions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["balance_metrics"] = self.balance_metrics

        return context


@method_decorator(login_required(), "dispatch")
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "pages/transactions/transaction_create.html"
    success_url = reverse_lazy("transaction_list")

    def form_valid(self, form):
        new_transaction = form.save(commit=False)
        new_transaction.account = self.request.user.account
        new_transaction.save()

        return super().form_valid(form)


@method_decorator(login_required(), "dispatch")
class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "pages/transactions/transaction_update.html"
    context_object_name = "transaction"
    success_url = reverse_lazy("transaction_list")

    def form_valid(self, form):
        new_transaction = form.save(commit=False)
        new_transaction.account = self.request.user.account
        new_transaction.save()

        return super().form_valid(form)


@method_decorator(login_required(), "dispatch")
class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = "pages/transactions/transaction_delete.html"
    context_object_name = "transaction"
    success_url = reverse_lazy("transaction_list")
