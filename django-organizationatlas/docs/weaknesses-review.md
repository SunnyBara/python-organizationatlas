# OrganizationAtlas — Revue des points faibles (métier & performance)

Revue de l'état actuel de `python-organizationatlas` (cœur) et `django-organizationatlas`
(intégration Django). Chaque point indique la **sévérité**, le **fichier**
concerné et une **piste de correction**. Les points sont triés par criticité.

Légende sévérité : 🔴 critique · 🟠 important · 🟡 mineur

---

## 3. Modélisation métier

### 🟠 3.1 — Relations : dimension quantitative encore manquante

✅ **Dimension temporelle traitée.** Un `TemporalValidityMixin`
(`models/temporal.py`) ajoute `valid_from` / `valid_to` (+ propriété
`is_current`) aux modèles de faits : `OrganizationAtlasData`, `OrganizationAtlasAddress`,
`OrganizationRelation`, `StakeholderRelation`. Le versionnement est garanti par
des contraintes d'unicité **partielles** (`WHERE valid_to IS NULL`) : une seule
version *ouverte* par clé logique. `create_source` applique le pattern
*supersede* (clôture l'ancienne version puis insère la nouvelle).

❌ **Reste la dimension quantitative.** Un actionnaire sans **% détenu** ou
**nombre de titres** ne permet toujours pas la logique de *cap table* ni le seuil
**bénéficiaire effectif 25 %** (réglementaire).

**Correction restante :** ajouter `percentage` / `shares_count` sur
`StakeholderRelation` (et le lien actionnaire).

### 🟠 3.2 — `gender` mélange genre et structure de détention

`Person.gender` inclut `indivision` aux côtés de `male`/`female`. Une indivision
n'est pas un genre mais une **co-détention** de personnes physiques. Mélanger les
deux pollue toute requête « propriétaires femmes » (il faut exclure
`indivision`/`undisclosed`) et empêche de représenter qui compose l'indivision.

**Correction :** séparer `gender` (identité de la personne) d'un éventuel
`ownership_structure` / `is_indivision`, ou modéliser l'indivision comme un
regroupement de personnes.

### 🟠 3.3 — Direction des relations ambiguë

Pour `OrganizationRelation`, le sens `from_organization → to_organization` est explicite
pour `branch_of`/`agency_of` (« from est une succursale de to ») mais **ambigu**
pour `parent_organization` : `from` est-il la mère ou la fille ? Aucune convention
documentée.

**Correction :** documenter la convention de sens, ou renommer les codes de façon
non ambiguë (`is_parent_of` / `is_subsidiary_of`).

### 🟠 3.4 — Workflow d'enrichissement non implémenté

`Organization.enrich()` retourne `False` (stub) et `admin/organization.py` →
`handle_refresh_person` fait `print("ok")`. Les 6 actions admin
(`refresh_data`, `refresh_address`, `full_refresh`, …) sont **déclarées mais non
fonctionnelles**.

**Correction :** implémenter le pipeline d'enrichissement ou retirer les actions
tant qu'elles ne font rien (UX trompeuse).

### 🟡 3.5 — `value_type` déclaratif sans cast ni validation

`OrganizationAtlasData.value` est un `TextField` et `value_type` (`str`/`int`/`float`/
`json`) n'est **jamais** appliqué : aucune validation à l'écriture, aucun
accesseur typé à la lecture. Rien n'empêche `value_type="int"` avec
`value="abc"`.

**Correction :** propriété `typed_value` qui caste selon `value_type`, +
validation dans `clean()`.

### 🟡 3.6 — Tout en `CASCADE`

La suppression d'une `Organization` détruit en cascade data, adresses, événements,
documents, personnes, et désormais relations/stakeholders. Pour un produit de
données « source de vérité », perdre l'historique au `DELETE` est risqué.

**Correction :** envisager le soft-delete (ou `PROTECT`/`SET_NULL`) sur les
entités à valeur historique.

---

## 4. Parité fonctionnelle France (rappel)

Le schéma provider (`FRANCE_FIELDS_DESCRIPTIONS`) et le modèle ne couvrent pas
encore les champs financiers/boursiers et qualitatifs de l'app legacy `organization/`
(`ape_noun`, `effective`, `isin`, `ticker`, `coderef`, `index`, `governance`,
`evaluation`, `quality_independent`, `siege`). Voir le détail et le plan dans
[`migration-from-organization.md`](./migration-from-organization.md) (sections B à F).

---

## 5. Synthèse priorisée

| # | Sévérité | Sujet | Effort |
|---|---|---|---|
| 2.5 | 🟠 | Migrations en attente | manuel |
| 3.1 | 🟠 | Relations : `% détenu` / `shares_count` restant | 30 min |
| 3.2 | 🟠 | `gender` mêlé à l'indivision | 30 min |
| 3.3 | 🟠 | Direction des relations ambiguë | 20 min |
| 3.4 | 🟠 | Enrichissement / refresh non implémenté | variable |
| 3.5 / 3.6 | 🟡 | cast `value_type`, soft-delete | divers |
