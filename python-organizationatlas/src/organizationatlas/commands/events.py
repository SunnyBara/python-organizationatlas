"""Organization events command."""

from organizationatlas.helpers import get_organization_events

from ._base import make_command

events_command = make_command(
    get_organization_events,
    api_command="get_organization_events",
    arg_name="code",
    description="Get organization events (use --code organization_code)",
)
