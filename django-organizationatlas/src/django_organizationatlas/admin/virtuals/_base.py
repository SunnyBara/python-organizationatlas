from django.contrib import admin


class ReadOnlyVirtualAdmin(admin.ModelAdmin):
    """Base admin for virtual (non-DB) models: no add/change/delete."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
