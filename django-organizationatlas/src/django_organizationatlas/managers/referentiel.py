from django.db import models
from django.db.models import Count


class OrganizationAtlasReferentielQuerySet(models.QuerySet):
    def with_usage_count(self):
        return self.annotate(sql_used_count=Count("to_organizationatlasdata"))


class OrganizationAtlasReferentielManager(models.Manager):
    def get_queryset(self):
        return OrganizationAtlasReferentielQuerySet(self.model, using=self._db)
