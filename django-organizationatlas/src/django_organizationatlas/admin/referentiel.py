from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.referentiel import OrganizationAtlasReferentiel
from ..models.source import ORGANIZATIONATLAS_FIELDS_SOURCE

base_fields = [
    "category",
    "usage_type",
    "code",
    "description",
    "characteristics",
    "priority",
    "used_count",
]


@admin.register(OrganizationAtlasReferentiel)
class OrganizationAtlasReferentielAdmin(AdminBoostModel):
    list_display = base_fields
    list_filter = ["category", "usage_type"]
    search_fields = ["category", "code", "description", "characteristics"]
    readonly_fields = ["created_at", "updated_at", "used_count"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_usage_count()

    def used_count(self, obj):
        return getattr(obj, "sql_used_count", "—")
    used_count.short_description = _("Used count")
    used_count.admin_order_field = "sql_used_count"

    def change_fieldsets(self):
        self.add_to_fieldset(None, base_fields)
        self.add_to_fieldset(_("Source"), ORGANIZATIONATLAS_FIELDS_SOURCE)
