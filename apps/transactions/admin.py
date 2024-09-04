from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("kind", "amount", "category", "account")
    list_per_page = 10

    fieldsets = (
        (_("Informações da transação"), {"fields": ("kind", "amount", "category", "account")}),
        (_("Datas importantes"), {"fields": ("created_at", "updated_at")}),
        (_("Identificadores"), {"fields": ("id", "slug")}),
    )
    add_fieldsets = ((None, {"fields": ("kind", "amount", "category", "account")}),)
    readonly_fields = ("id", "slug", "created_at", "updated_at")

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
