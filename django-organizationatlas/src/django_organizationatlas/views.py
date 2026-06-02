"""Views for organizationatlas app."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import OrganizationAtlasOrganization


def organization_list(request):
    """List all organizations."""
    organizations = OrganizationAtlasOrganization.objects.all()
    context = {
        "organizations": organizations,
    }
    return render(request, "django_organizationatlas/organization_list.html", context)


def organization_detail(request, pk):
    """Show organization details."""
    organization = get_object_or_404(OrganizationAtlasOrganization, pk=pk)
    context = {
        "organization": organization,
    }
    return render(request, "django_organizationatlas/organization_detail.html", context)


def organization_enrich(request, pk):
    """Trigger organization enrichment."""
    organization = get_object_or_404(OrganizationAtlasOrganization, pk=pk)

    if request.method == "POST":
        if organization.enrich(force=True):
            messages.success(request, f"Successfully enriched {organization.denomination}")
        else:
            messages.error(request, f"Failed to enrich {organization.denomination}")
        return redirect("django_organizationatlas:organization-detail", pk=pk)

    return render(request, "django_organizationatlas/organization_enrich.html", {"organization": organization})
