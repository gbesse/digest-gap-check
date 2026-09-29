# Digest Gap Check

**Revise artículos AIHOT seleccionados pero ausentes como enlaces individuales de un boletín diario.**

[English](README.md) · [Français](README.fr.md) · Español

## Ver el problema con un comando

```sh
python3 audit.py demo --lang es
```

El ejemplo distingue un artículo incluido, un caso para revisar y un artículo no seleccionado.

## Proyectos cercanos

- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT) — Sus API públicas de boletines y artículos son la integración real; sin afiliación.
- [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT/pull/1) — Corrige omisiones entre periodos; esta herramienta ofrece una lista para revisar.
- [www.feedvalidator.org](https://www.feedvalidator.org/) — Valida la sintaxis de fuentes; esta herramienta compara etapas de publicación.

## Usarlo con sus datos

```sh
python3 audit.py run --date 2026-09-29 --base-url https://aihot.news --lang es
```

El adaptador usa las API públicas de AIHOT `/api/v1/dailies/<date>` y `/api/v1/items?mode=selected` con paginación. Compara ID dentro del periodo y muestra enlaces para revisión. `--json` produce resultados estructurados.

## Alcance y límites

La ausencia de un enlace individual no prueba un fallo: un artículo puede excluirse o agruparse deliberadamente. La API pública cubre siete días móviles; ejecute pronto la comprobación. El límite de paginación señala un análisis incompleto.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licencia MIT. La demo no requiere cuenta ni clave API.
