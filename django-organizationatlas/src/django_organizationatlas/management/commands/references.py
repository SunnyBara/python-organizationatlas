from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from django_organizationatlas.services.references import (
    export_references_to_path,
    import_references_from_path,
)


class Command(BaseCommand):
    help = "Import or export references as CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--upload",
            nargs="?",
            const="",
            default=None,
            help="Export references to a CSV file. Defaults to references/upload/dump.csv",
        )
        parser.add_argument(
            "--download",
            nargs="?",
            const="",
            default=None,
            help="CSV file or directory to import. Defaults to references/download/*.csv",
        )

    def handle(self, **options):
        upload = options.get("upload")
        download = options.get("download")

        if upload is not None and download is not None:
            raise CommandError("Use either --upload or --download, not both")

        if upload is None and download is None:
            raise CommandError("Use --upload or --download")

        if upload is not None:
            path = upload or Path.cwd() / "references" / "upload"
            dump_path, exported_count = export_references_to_path(path)
            self.stdout.write(
                self.style.SUCCESS(f"Exported {exported_count} reference(s) to {dump_path}")
            )
        else:
            path = download or Path.cwd() / "references" / "download"
            created_count, updated_count, file_count = import_references_from_path(path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported {file_count} file(s): {created_count} created, {updated_count} updated"
                )
            )
