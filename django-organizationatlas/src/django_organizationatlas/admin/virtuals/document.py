from django.contrib import admin

from ...models.virtuals.document import OrganizationAtlasVirtualDocument
from ._base import ReadOnlyVirtualAdmin


@admin.register(OrganizationAtlasVirtualDocument)
class OrganizationAtlasVirtualDocumentAdmin(ReadOnlyVirtualAdmin):
    list_display = ["__str__"]
    readonly_fields = []
