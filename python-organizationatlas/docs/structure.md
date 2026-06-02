## Project Structure

OrganizationAtlas follows a standard Python package structure with a provider-based architecture using ProviderKit for provider management.

### General Structure

```
python-organizationatlas/
├── src/
│   └── organizationatlas/          # Main package directory
│       ├── __init__.py        # Package exports
│       ├── providers/         # Organization data provider implementations
│       │   ├── __init__.py    # OrganizationAtlasProvider base class
│       │   └── ...            # Provider implementations
│       ├── commands/           # Command infrastructure
│       ├── helpers.py          # Helper functions (get_organization_providers, search_organizations, etc.)
│       ├── cli.py              # CLI interface
│       └── __main__.py         # Entry point for package execution
├── tests/                     # Test suite
│   └── ...
├── docs/                      # Documentation
│   └── ...
├── service.py                 # Main service entry point script
├── pyproject.toml             # Project configuration
└── ...
```

### Module Organization Principles

- **Single Responsibility**: Each module should have a clear, single purpose
- **Separation of Concerns**: Keep different concerns in separate modules
- **Provider-Based Architecture**: Providers inherit from ProviderKit's ProviderBase
- **Clear Exports**: Use `__init__.py` to define public API
- **Logical Grouping**: Organize related functionality together

### Provider Organization

The `providers/` directory contains organization data provider implementations:

- **`__init__.py`**: Defines `OrganizationAtlasProvider` base class that extends `ProviderBase` from ProviderKit
- Each provider file implements a specific organization data service
- All providers inherit from `OrganizationAtlasProvider` which provides common functionality

### Helper Functions

The `helpers.py` module provides:
- `get_organizationatlas_providers()`: Get organization providers from various sources
- `get_organizationatlas_provider()`: Get a single organization provider by attribute search
- `search_organization()`: Search organizations using providers
- `search_organization_by_reference()`: Get organization by reference ID (SIREN, SIRET, RNA, etc.)
- `get_organization_documents()`: Get organization documents using providers
- `get_organization_events()`: Get organization events using providers
- `get_organization_officers()`: Get organization officers using providers
- `get_ultimate_beneficial_owners()`: Get ultimate beneficial owners using providers

### Package Exports

The public API is defined in `src/organizationatlas/__init__.py`:
- Provider base class and helper functions

### ProviderKit Integration

OrganizationAtlas uses ProviderKit for provider management:
- Providers inherit from `ProviderBase` via `OrganizationAtlasProvider`
- Uses ProviderKit's helper functions for provider discovery and management
- Providers can be loaded from JSON, configuration, or directory scanning
