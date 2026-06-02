from typing import Any, cast

import requests

from . import OrganizationAtlasFranceProvider


class InpiProvider(OrganizationAtlasFranceProvider):
    name = "inpi"
    display_name = "INPI"
    description = "Institut National de la Propriété Industrielle - Registre national des entreprises"
    required_packages = ["requests"]
    config_keys = ["API_USERNAME", "API_PASSWORD", "BASE_URL", "SSO_URL"]
    config_defaults = {
        "BASE_URL": "https://registre-national-entreprises.inpi.fr",
        "SSO_URL": "https://registre-national-entreprises.inpi.fr/api/sso/login",
    }
    documentation_url = "https://www.inpi.fr/fr/services-et-outils/api"
    site_url = "https://www.inpi.fr"
    status_url = None
    priority = 5

    _address_prefixes = (
        "formality.content.personneMorale.adresseEntreprise.adresse",
        "formality.content.personneMorale.etablissementPrincipal.adresse",
        "formality.content.personnePhysique.etablissementPrincipal.adresse",
        "formality.content.personnePhysique.adresseEntreprise.adresse",
    )

    fields_associations = {
        "reference": (
            "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.siret",
            "siren",
            "formality.siren",
            "formality.content.personneMorale.identite.entreprise.siren",
        ),
        "denomination": (
            "formality.content.personnePhysique.etablissementPrincipal.descriptionEtablissement.nomCommercial",
            "formality.content.personneMorale.identite.entreprise.denomination",
            "formality.content.personnePhysique.etablissementPrincipal.descriptionEtablissement.nomCommercial",
            "formality.content.personnePhysique.identite.entreprise.denomination",
        ),
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._token: str | None = None

    def _get_token(self) -> str | None:
        if self._token:
            return self._token
        username = self._get_config_or_env("API_USERNAME")
        password = self._get_config_or_env("API_PASSWORD")
        if not username or not password:
            return None
        try:
            response = requests.post(
                self._get_config_or_env("SSO_URL"),
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            self._token = data.get("token") or data.get("access_token")
            return self._token
        except Exception:
            return None

    def _call_api(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[dict[str, Any]] | None:
        token = self._get_token()
        if not token:
            return None
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return cast("dict[str, Any] | list[dict[str, Any]]", response.json())

    def get_normalize_address(self, data: dict[str, Any]) -> str | None:
        for prefix in self._address_prefixes:
            addr = self._get_nested_value(data, prefix)
            if addr:
                return self._build_address_str(
                    addr.get("numVoie"),
                    addr.get("typeVoie"),
                    addr.get("voie"),
                    addr.get("codePostal"),
                    addr.get("commune"),
                    complementLocalisation=addr.get("complementLocalisation"),
                )
        return None

    def _build_address_str(self, numero, type_voie, libelle, code_postal, commune, country=None, complementLocalisation=None):
        line1 = [p for p in [numero, type_voie, libelle] if p]
        line2_parts = [p for p in [str(code_postal) if code_postal else None, commune] if p]
        ad1 = " ".join(str(p) for p in line1) if line1 else None
        ad2 = " ".join(line2_parts) if line2_parts else None
        parts = [f for f in [ad1, complementLocalisation, ad2] if f]
        return ", ".join(parts) if parts else None

    def get_normalize_description(self, data: dict[str, Any]) -> str | None:
        activite = (
            self._get_nested_value(data, "formality.content.personneMorale.identite.entreprise.activitePrincipale")
            or self._get_nested_value(data, "formality.content.personnePhysique.identite.entreprise.activitePrincipale")
        )
        nature = (
            self._get_nested_value(data, "formality.content.personneMorale.identite.entreprise.natureJuridique")
            or self._get_nested_value(data, "formality.content.personnePhysique.identite.entreprise.natureJuridique")
        )
        parts = [p for p in [activite, nature] if p]
        return " - ".join(parts) if parts else None

    def search_organization(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        if not query:
            return []
        result = self._call_api(
            f"{self._get_config_or_env('BASE_URL')}/api/organizations",
            params={"organizationName": query, "page": 1, "pageSize": 20},
        )
        if not result:
            return []
        if isinstance(result, dict):
            return result.get("organizations") or result.get("data") or []
        if isinstance(result, list):
            return result
        return []

    def search_organization_by_reference(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        return self._call_api(f"{self._get_config_or_env('BASE_URL')}/api/organizations/{siren}")
