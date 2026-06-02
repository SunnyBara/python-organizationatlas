"""Organization search by reference command."""

from organizationatlas.helpers import search_organization_by_reference

from ._base import make_command

code_command = make_command(
    search_organization_by_reference,
    api_command="search_organization_by_reference",
    arg_name="code",
    description="Search organization by reference (use --code organization_code)",
    with_readable=True,
)
