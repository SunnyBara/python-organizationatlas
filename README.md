# OrganizationAtlas

Monorepo contenant **organizationatlas** (bibliothèque Python pour la recherche d'entreprises) et **django-organizationatlas** (intégration Django).

## Packages

### organizationatlas — `python-organizationatlas/`

Bibliothèque Python pour la recherche et l'enrichissement d'informations entreprises. Interface unifiée vers plusieurs fournisseurs de données (Pappers, societe.com, etc.) via ProviderKit.

- **Recherche d'entreprises** : par nom, domaine ou identifiant
- **Enrichissement** : documents, événements, dirigeants, UBO
- **Format normalisé** : structure de champs cohérente entre les providers

📁 Docs : [python-organizationatlas/docs/](python-organizationatlas/docs/)

### django-organizationatlas — `django-organizationatlas/`

Intégration Django pour OrganizationAtlas. Champs, widgets, admin.

📁 Docs : [django-organizationatlas/docs/](django-organizationatlas/docs/)

## Structure du dépôt

```
organizationatlas/
├── python-organizationatlas/   # Bibliothèque core
├── django-organizationatlas/    # Intégration Django
└── README.md
```

## Développement

Chaque package a son propre `service.py` :

```bash
# Dans python-organizationatlas/ ou django-organizationatlas/
./service.py dev install-dev
./service.py dev test
./service.py quality lint
```

## Licence

MIT
