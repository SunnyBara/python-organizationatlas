"""Organization search command."""

from organizationatlas.helpers import search_organization

from ._base import make_command

search_command = make_command(
    search_organization,
    api_command="search_organization",
    arg_name="query",
    description="Search organizations (use --query query_string)",
    with_readable=True,
)
