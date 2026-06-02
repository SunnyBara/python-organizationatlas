import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from django_organizationatlas.models import OrganizationAtlasReferentiel as Referentiel

TRANSLATION_PREFIXES = ("name", "description", "characteristics")


def _extract_translations(row: dict) -> dict:
    """Return a dict of all i18n columns, e.g. {'name_fr': '...', 'description_en': '...'}."""
    return {
        key: value
        for key, value in row.items()
        if any(key.startswith(f"{prefix}_") for prefix in TRANSLATION_PREFIXES)
        and value
    }


class Command(BaseCommand):
    help = "Load Referentiel data from one CSV file or all CSVs in data_sources/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            help="Path to a specific CSV file. Defaults to all *.csv in data_sources/",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing Referentiel data before loading",
        )
        parser.add_argument(
            "--usage-type",
            type=str,
            choices=["description", "configuration", "characteristics"],
            help="Usage type for all loaded records (overridden by CSV column if present)",
        )

    def handle(self, **options):
        if options["csv"]:
            csv_paths = [Path(options["csv"])]
        else:
            data_sources_dir = Path(__file__).parent.parent.parent / "data_sources"
            csv_paths = sorted(data_sources_dir.rglob("*.csv"))

        if not csv_paths:
            self.stdout.write(self.style.ERROR("No CSV files found."))
            return

        if options["clear"]:
            count = Referentiel.objects.count()
            Referentiel.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {count} existing Referentiel records"))

        total_created = 0
        total_updated = 0

        for csv_path in csv_paths:
            if not csv_path.exists():
                self.stdout.write(self.style.ERROR(f"File not found: {csv_path}"))
                continue

            self.stdout.write(f"\nLoading {csv_path.relative_to(csv_path.parent.parent.parent) if csv_path.is_absolute() else csv_path} ...")
            created_count, updated_count = self._load_csv(csv_path, options)
            total_created += created_count
            total_updated += updated_count

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone: {total_created} created, {total_updated} updated across {len(csv_paths)} file(s)"
            )
        )

    def _load_csv(self, csv_path: Path, options: dict) -> tuple[int, int]:
        created_count = 0
        updated_count = 0

        with open(csv_path, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if not row.get("code"):
                    continue

                # Base fields
                data = {
                    "category": row.get("category", ""),
                    "description": row.get("description", ""),
                    "characteristics": row.get("characteristics", ""),
                    "priority": int(row.get("priority") or 0),
                }

                # usage_type: CSV column takes priority over CLI argument
                if row.get("usage_type"):
                    data["usage_type"] = row["usage_type"]
                elif options.get("usage_type"):
                    data["usage_type"] = options["usage_type"]

                # Build metadata: base name + all i18n columns (name_fr, description_en, …)
                metadata = {}
                if row.get("name"):
                    metadata["name"] = row["name"]
                metadata.update(_extract_translations(row))
                if metadata:
                    data["metadata"] = metadata

                obj, created = Referentiel.objects.update_or_create(
                    code=row["code"],
                    defaults=data,
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"  Created: {row['code']}"))
                else:
                    updated_count += 1
                    self.stdout.write(f"  Updated: {row['code']}")

        return created_count, updated_count
