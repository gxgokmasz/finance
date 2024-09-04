from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse as HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from apps.transactions.metrics import TransactionsMetrics


@method_decorator(login_required(), "dispatch")
class DashboardView(TemplateView):
    template_name = "pages/home/dashboard.html"

    def initialize_requests_common_data(self, request, *args, **kwargs):
        transactions_metrics = TransactionsMetrics(request.user)

        self.balance_metrics = transactions_metrics.get_balance_metrics()

    def get(self, request, *args, **kwargs) -> HttpResponse:
        self.initialize_requests_common_data(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["balance_metrics"] = self.balance_metrics

        return context
