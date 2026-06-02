from typing import Any

from organizationatlas.helpers import get_organization_events

from .base import OrganizationAtlasVirtualCommandManager


class OrganizationAtlasVirtualEventManager(OrganizationAtlasVirtualCommandManager):
    """Manager for organization events from organizationatlas."""

    _command = "get_organization_events"
    _commands = {"get_organization_events": get_organization_events}

    def get_organization_events(self, code: str, first: bool = False, **kwargs: Any) -> Any:
        return self.get_queryset_command("get_organization_events", code=code, first=first, **kwargs)
