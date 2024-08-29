from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin, ProcessFormView
from django.views.generic.list import ListView
from .forms import TransactionForm
from .metrics import TransactionsMetrics
from .models import Transaction


@method_decorator(login_required(), "dispatch")
class DashboardView(ListView, FormMixin, ProcessFormView):
    model = Transaction
    form_class = TransactionForm
    template_name = "pages/transactions/dashboard.html"
    context_object_name = "transactions"
    success_url = reverse_lazy("home")
    paginate_by = 6

    def initialize_requests_common_data(self, request, *args, **kwargs):
        transactions_metrics = TransactionsMetrics(request.user)

        self.balance_metrics = transactions_metrics.get_balance_metrics()
        self.currency_percentages = transactions_metrics.get_currency_percentages()
        self.weekly_xip_relationship = transactions_metrics.get_weekly_xip_relationship()
        self.object_list = super().get_queryset(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.initialize_requests_common_data(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.initialize_requests_common_data(request, *args, **kwargs)

        transaction_to_delete_uuid = request.POST.get("transaction_to_delete")

        if transaction_to_delete_uuid:
            transaction_to_delete = Transaction.objects.filter(
                slug=transaction_to_delete_uuid
            ).first()

            if transaction_to_delete:
                transaction_to_delete.delete()

            return HttpResponseRedirect(reverse_lazy("home"))

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        new_transaction = form.save(commit=False)
        new_transaction.account = self.request.user.account

        new_transaction.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        has_amount_errors = form.errors.get("amount")
        has_category_errors = form.errors.get("category")
        has_genre_errors = form.errors.get("genre")

        amount_errors = has_amount_errors.data[0] if has_amount_errors else []

        category_errors = has_category_errors.data[0] if has_category_errors else []

        genre_errors = has_genre_errors.data[0] if has_genre_errors else []

        errors = [*amount_errors, *category_errors, *genre_errors]

        for error in errors:
            messages.add_message(self.request, messages.ERROR, error)

        return super().form_invalid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset_filtered_by_account = queryset.filter(account=self.request.user.account)

        transaction_search = self.request.GET.get("transaction_search")

        if transaction_search:
            queryset_filtered_by_category = queryset_filtered_by_account.filter(
                category__icontains=transaction_search
            )

            return queryset_filtered_by_category

        return queryset_filtered_by_account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["new_transaction_form"] = TransactionForm()
        context["balance_metrics"] = self.balance_metrics
        context["currency_percentages"] = self.currency_percentages
        context["weekly_xip_relationship"] = self.weekly_xip_relationship

        return context
