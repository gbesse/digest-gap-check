# Digest Gap Check

**Repérez les articles AIHOT sélectionnés mais absents des liens individuels d’un bulletin quotidien.**

[English](README.md) · Français · [Español](README.es.md)

## Voir le problème en une commande

```sh
python3 audit.py demo --lang fr
```

La fixture distingue un article inclus, un candidat à examiner et un article non sélectionné.

**Exemple de sortie**

```text
Articles sélectionnés absents du bulletin
Exemple hors ligne ; run utilise l'API publique AIHOT.
Candidats à revoir, pas des omissions techniques prouvées.
candidate: Selected but absent — https://aihot.news/items/candidate
```

## Projets voisins

- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT) — Ses API publiques de bulletins et d’articles constituent l’intégration réelle ; aucune affiliation.
- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT/pull/1) — Corrige des omissions entre périodes ; cet outil donne une liste à examiner.
- [www.feedvalidator.org](https://www.feedvalidator.org/) — Valide la syntaxe des flux ; cet outil compare des étapes de publication.

## Utiliser vos données

```sh
python3 audit.py run --date 2026-09-29 --base-url https://aihot.news --lang fr
```

L’adaptateur utilise les API publiques AIHOT `/api/v1/dailies/<date>` et `/api/v1/items?mode=selected` paginée. Il compare les ID dans la période du bulletin et fournit des liens à examiner. `--json` produit un résultat structuré.

## Périmètre et limites

L’absence de lien individuel ne prouve pas un bug : un article peut être exclu ou regroupé volontairement. L’API publique couvre sept jours glissants ; lancez le contrôle rapidement. La limite de pagination signale un balayage incomplet.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licence MIT. La démo ne demande ni compte ni clé API.

## Correspondance des liens

Un lien du bulletin avec paramètres, fragment ou barre finale correspond toujours au même article. Un chemin imbriqué comme `/items/id/comments` ne compte pas comme lien individuel. Exécutez la démo hors ligne pour examiner les candidats.
