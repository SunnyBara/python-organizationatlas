"""Helper functions for organization data management."""

from django.db import transaction

from .models import (
    OrganizationAtlasAddress,
    OrganizationAtlasOrganization,
    OrganizationAtlasData,
)

# Fields on the virtual organization object that should not be persisted as OrganizationAtlasData.
# Everything else (siren, siret, ape, legalform, …) will be persisted if non-empty.
_SKIP_FIELDS = frozenset({
    "organizationatlas_id",
    "reference",       # persisted via source_field key
    "address",         # persisted as OrganizationAtlasAddress
    "address_json",
    "data_source",
    "backend",
    "backend_name",
    "country_code",    # stored on the record itself, not as data
    "source_field",    # used as key, not value
})


def _iter_data_fields(obj) -> dict:
    """Return {data_type: value} for every non-empty, non-system field on obj."""
    result = {}
    for field in getattr(obj, "_meta", None) and obj._meta.get_fields() or []:
        name = getattr(field, "name", None) or getattr(field, "attname", None)
        if not name or name in _SKIP_FIELDS:
            continue
        value = getattr(obj, name, None)
        if value is None or value == "":
            continue
        result[name] = str(value)
    return result


@transaction.atomic
def create_organization(obj):
    organization = OrganizationAtlasOrganization.objects.create(
        denomination=obj.denomination,
        code=obj.reference,
        source=obj.backend,
        country_code=obj.country_code,
    )

    # Persist the canonical identifier first (e.g. siren, siret, rna)
    OrganizationAtlasData.objects.update_or_create(
        organization=organization,
        source=obj.backend,
        country_code=obj.country_code or "",
        data_type=obj.source_field,
        defaults={"value": obj.reference},
    )

    # Persist every enrichment field available on the virtual object
    for data_type, value in _iter_data_fields(obj).items():
        if data_type == obj.source_field:
            continue  # already persisted above
        OrganizationAtlasData.objects.update_or_create(
            organization=organization,
            source=obj.backend,
            country_code=obj.country_code or "",
            data_type=data_type,
            defaults={"value": value},
        )

    # Address — guard against address_json being None even when address string is set
    if obj.address_json:
        OrganizationAtlasAddress.objects.create(
            organization=organization,
            source=obj.backend,
            country_code=obj.country_code,
            address=obj.address_json,
            is_headquarters=True,
        )

    return organization
