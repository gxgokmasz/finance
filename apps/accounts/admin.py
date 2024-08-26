from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user",)
    list_per_page = 10

    fieldsets = (
        (_("Informações da conta"), {"fields": ("user",)}),
        (_("Datas importantes"), {"fields": ("created_at", "updated_at")}),
        (_("Identificadores"), {"fields": ("id", "slug")}),
    )
    add_fieldsets = ((None, {"fields": ("user",)}),)
    readonly_fields = ("id", "slug", "created_at", "updated_at")

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
