"""Organization documents command."""

from organizationatlas.helpers import get_organization_documents

from ._base import make_command

documents_command = make_command(
    get_organization_documents,
    api_command="get_organization_documents",
    arg_name="code",
    description="Get organization documents (use --code organization_code)",
)
