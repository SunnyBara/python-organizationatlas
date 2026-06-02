from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.data import OrganizationAtlasData
from ..models.source import ORGANIZATIONATLAS_FIELDS_SOURCE


@admin.register(OrganizationAtlasData)
class OrganizationAtlasDataAdmin(AdminBoostModel):
    list_display = ["organization", "data_type", "value", "created_at"]
    list_filter = ["data_type", "created_at"]
    search_fields = ["organization__denomination", "data_type", "value"]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["organization"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, ('organization', 'data_type', 'value_type', 'value', ))
        self.add_to_fieldset(_("Source"), ORGANIZATIONATLAS_FIELDS_SOURCE)


class OrganizationAtlasDataInline(admin.TabularInline):
    model = OrganizationAtlasData
    extra = 1
    fields = ["data_type", "value_type", "value", "source", "country_code"]
