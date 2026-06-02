from django.contrib import admin

from ...models.virtuals.event import OrganizationAtlasVirtualEvent
from ._base import ReadOnlyVirtualAdmin


@admin.register(OrganizationAtlasVirtualEvent)
class OrganizationAtlasVirtualEventAdmin(ReadOnlyVirtualAdmin):
    list_display = ["__str__"]
    readonly_fields = []
