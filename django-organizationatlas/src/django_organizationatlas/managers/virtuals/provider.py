"""Manager for organizationatlas providers."""


from django_providerkit.managers import BaseProviderManager


class OrganizationAtlasProviderManager(BaseProviderManager):
    """Manager for organizationatlas providers."""
    package_name = 'organizationatlas'
