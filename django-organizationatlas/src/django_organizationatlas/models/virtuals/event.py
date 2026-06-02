from django.db import models
from django.utils.translation import gettext_lazy as _

from ...managers.virtuals.event import OrganizationAtlasVirtualEventManager


class OrganizationAtlasVirtualEvent(models.Model):
    """Virtual event model for organizationatlas."""

    objects = OrganizationAtlasVirtualEventManager()

    class Meta:
        managed = False
        verbose_name = _("Virtual Event")
        verbose_name_plural = _("Virtual Events")

