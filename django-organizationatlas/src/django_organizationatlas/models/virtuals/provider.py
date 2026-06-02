"""Provider model for organizationatlas providers."""

from organizationatlas.helpers import ADD_FIELDS
from organizationatlas.providers import OrganizationAtlasProvider
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_providerkit.models.define import define_provider_fields, define_service_fields
from virtualqueryset.models import VirtualModel

from ...managers.virtuals.provider import OrganizationAtlasProviderManager

_default_cfg = getattr(OrganizationAtlasProvider, '_default_services_cfg', {})
services_cfg = getattr(OrganizationAtlasProvider, 'services_cfg', _default_cfg)
services = list(services_cfg.keys())

@define_provider_fields(primary_key='name', add_fields=ADD_FIELDS)
@define_service_fields(services)
class OrganizationAtlasProviderModel(VirtualModel):
    """Virtual model for organizationatlas providers."""

    name: models.CharField = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Provider name (e.g., insee)"),
        primary_key=True,
    )

    objects = OrganizationAtlasProviderManager(package_name='organizationatlas')

    class Meta:
        managed = False
        app_label = 'django_organizationatlas'
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")
        ordering = ['-priority', 'name']

    def __str__(self) -> str:
        return self.display_name or self.name
