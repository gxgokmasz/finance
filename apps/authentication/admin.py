from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_per_page = 10

    fieldsets = (
        (_("Informações do usuário"), {"fields": ("username", "password", "email")}),
        (
            _("Permissões"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined", "updated_at")}),
        (_("Identificadores"), {"fields": ("id", "slug")}),
    )
    add_fieldsets = ((None, {"fields": ("username", "email", "password1", "password2")}),)
    readonly_fields = ("id", "slug", "date_joined", "updated_at", "last_login")

    form = UserChangeForm
    add_form = UserCreationForm
