## Project Structure

django-organizationatlas follows a standard Python package structure with Django integration for OrganizationAtlas.

### General Structure

```
django-organizationatlas/
├── src/
│   └── django_organizationatlas/        # Main package directory
│       ├── __init__.py        # Package exports
│       ├── models/            # Django model definitions
│       ├── models.py          # Model definitions
│       ├── managers/          # Custom managers
│       ├── admin/             # Django admin configuration
│       ├── views.py           # Django views
│       ├── urls.py             # URL configuration
│       ├── helpers.py          # Helper functions
│       ├── apps.py             # Django app configuration
│       └── templates/          # Django templates
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
- **Django Integration**: Integrates OrganizationAtlas with Django's ORM and admin
- **Clear Exports**: Use `__init__.py` to define public API

### Model Organization

The `models/` directory and `models.py` contain Django model definitions for organization data.

### Manager Organization

The `managers/` directory contains custom managers for organization models.

### Admin Organization

The `admin/` directory contains Django admin configurations for organization models.

### Package Exports

The public API is defined in `src/django_organizationatlas/__init__.py`:
- Models, managers, and admin configurations

### OrganizationAtlas Integration

django-organizationatlas integrates OrganizationAtlas with Django:
- Uses OrganizationAtlas providers for organization data lookup
- Provides Django models and admin interface for organization data
- Integrates organization lookup and enrichment in Django applications
