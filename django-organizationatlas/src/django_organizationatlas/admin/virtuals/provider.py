"""Admin for provider model."""

from django.contrib import admin
from django_providerkit.admin.provider import BaseProviderAdmin

from ...models.virtuals.provider import OrganizationAtlasProviderModel
from ._base import ReadOnlyVirtualAdmin


@admin.register(OrganizationAtlasProviderModel)
class OrganizationAtlasProviderModelAdmin(ReadOnlyVirtualAdmin, BaseProviderAdmin):
    """Admin for organizationatlas providers."""

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display.insert(1, "geo_data")
        return list_display

    def change_fieldsets(self):
        super().change_fieldsets()
        self.add_to_fieldset(None, ["geo_data"])


__all__ = ["OrganizationAtlasProviderModelAdmin"]
