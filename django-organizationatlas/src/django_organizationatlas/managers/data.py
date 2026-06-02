from django.db import models
from django.db.models import OuterRef, Subquery

from ..models.referentiel import OrganizationAtlasReferentiel


class OrganizationAtlasDataQuerySet(models.QuerySet):
    def with_referentiel_description(self):
        return self.annotate(
            sql_referentiel_description=Subquery(
                OrganizationAtlasReferentiel.objects.filter(
                    pk=OuterRef("referentiel"),
                ).values("description")[:1],
            ),
        )


class OrganizationAtlasDataManager(models.Manager):
    def get_queryset(self):
        return OrganizationAtlasDataQuerySet(self.model, using=self._db)
