from django.contrib import admin
from .models import Solution


class ReadOnlyAdminMixin:
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Solution)
class SolutionAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "status",
    )
