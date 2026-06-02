from typing import Any

from organizationatlas.helpers import get_organization_documents

from .base import OrganizationAtlasVirtualCommandManager


class OrganizationAtlasVirtualDocumentManager(OrganizationAtlasVirtualCommandManager):
    """Manager for organization documents from organizationatlas."""

    _command = "get_organization_documents"
    _commands = {"get_organization_documents": get_organization_documents}

    def get_organization_documents(self, code: str, first: bool = False, **kwargs: Any) -> Any:
        return self.get_queryset_command("get_organization_documents", code=code, first=first, **kwargs)
