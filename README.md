# Digest Gap Check

**Review AIHOT items marked selected but absent as individual links from a daily bulletin.**

English · [Français](README.fr.md) · [Español](README.es.md)

## See the problem in one command

```sh
python3 audit.py demo --lang en
```

The offline fixture distinguishes an included article, a review candidate and an unselected article.

## Related projects

- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT) — Its published daily and items APIs are the live integration used here; there is no affiliation.
- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT/pull/1) — Fixes omissions across report periods; this tool gives operators a review list.
- [www.feedvalidator.org](https://www.feedvalidator.org/) — Validates feed syntax, while this tool compares publication stages.

## Use it on your data

```sh
python3 audit.py run --date 2026-09-29 --base-url https://aihot.news --lang en
```

The adapter uses AIHOT’s public `/api/v1/dailies/<date>` and paginated `/api/v1/items?mode=selected` endpoints. It compares article IDs within the report window and prints candidates with links. `--json` emits structured results.

## Scope and limits

An absent individual link is not proof of a bug: editors may intentionally omit or group an article. The public items API covers a rolling seven days; run promptly. A pagination cap produces an incomplete-scan warning.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. MIT. No account or API key is required for the demo.
