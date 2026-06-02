from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ..models.event import OrganizationAtlasEvent


class OrganizationEventInline(admin.TabularInline):
    model = OrganizationAtlasEvent
    extra = 1
    fields = ["source", "country_code", "event_type", "title", "date"]


@admin.register(OrganizationAtlasEvent)
class OrganizationEventAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "source",
        "country_code",
        "event_type",
        "title",
        "date",
        "created_at",
    ]
    list_filter = ["source", "country_code", "event_type", "date", "created_at"]
    search_fields = ["organization__denomination", "title", "event_type", "source"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            _("Event"),
            {"fields": ("organization", "source", "country_code", "event_type", "title", "date")},
        ),
        (_("Description"), {"fields": ("description",)}),
        (
            _("Metadata"),
            {"fields": ("metadata", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

