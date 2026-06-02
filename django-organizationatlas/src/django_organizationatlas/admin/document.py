from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.document import OrganizationAtlasDocument


class OrganizationDocumentInline(admin.TabularInline):
    model = OrganizationAtlasDocument
    extra = 1
    fields = ["source", "country_code", "document_type", "title", "date", "url"]


@admin.register(OrganizationAtlasDocument)
class OrganizationDocumentAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "source",
        "country_code",
        "document_type",
        "title",
        "date",
        "created_at",
    ]
    list_filter = ["source", "country_code", "document_type", "date", "created_at"]
    search_fields = ["organization__denomination", "title", "document_type", "source"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            _("Document"),
            {
                "fields": (
                    "organization",
                    "source",
                    "country_code",
                    "document_type",
                    "title",
                    "date",
                    "url",
                )
            },
        ),
        (_("Content"), {"fields": ("content",)}),
        (
            _("Metadata"),
            {"fields": ("metadata", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

