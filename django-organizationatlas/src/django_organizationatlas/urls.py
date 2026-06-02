"""URL configuration for organizationatlas app."""

from django.urls import path

from . import views

app_name = "django_organizationatlas"

urlpatterns = [
    path("", views.organization_list, name="organization-list"),
    path("<int:pk>/", views.organization_detail, name="organization-detail"),
    path("<int:pk>/enrich/", views.organization_enrich, name="organization-enrich"),
]
