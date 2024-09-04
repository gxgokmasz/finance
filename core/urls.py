from django.contrib import admin
from django.urls import include, path
from .common.views import DashboardView


urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("", DashboardView.as_view(), name="home"),
    path("", include("apps.authentication.urls")),
    path("", include("apps.transactions.urls")),
]
