# digest-gap-check — contrôle d’adoption · adoption check · comprobación de adopción

## Français

Point de départ local, après la préparation indiquée dans le README :

```sh
python3 audit.py demo --lang en
```

Un lien d’article avec paramètres peut désigner le même article, mais une page de commentaires ne prouve pas que l’article figure dans le bulletin. Examinez les candidats avant de conclure à un manque.

## English

Local starting point, after the setup described in the README:

```sh
python3 audit.py demo --lang en
```

An article URL with query parameters can identify the same item, but a comments page does not prove the article appears in the bulletin. Review candidates before calling an omission.

## Español

Punto de partida local, después de la preparación descrita en el README:

```sh
python3 audit.py demo --lang en
```

Una URL de artículo con parámetros puede identificar el mismo elemento, pero una página de comentarios no prueba que esté en el boletín. Revise los candidatos antes de declarar una omisión.
## Variante synthétique · Synthetic variation · Variante sintética

```text
/items/42?utm_source=mail ; /items/42/comments
```

FR : adaptez une copie de la fixture locale à cette situation, puis vérifiez le comportement décrit ci-dessus. Les valeurs sont illustratives, pas des résultats Jev mesurés.

EN: adapt a copy of the local fixture to this situation, then check the behavior described above. Values are illustrative, not measured Jev output.

ES: adapte una copia de la fixture local a esta situación y compruebe el comportamiento descrito arriba. Los valores son ilustrativos, no resultados Jev medidos.
