# Tarjeta 39 · E9, brecha train/test

Fecha: 2026-11-06  
`docs/informe-lncs.md` no está en el proyecto. La figura que pide es la Fig. 7.

## Estado

Cerrada. `construir_fig7` está en la sección 5 del notebook. La figura es `figuras/fig7_brecha_train_test.png` y los números están en `informe/seccion3.md`, sección 3.10.

| | Train | Test | Brecha |
|---|---|---|---|
| DT sin poda | 1,0000 ± 0,0000 | 0,9269 ± 0,0219 | 0,0731 |
| DT con poda | 0,9902 ± 0,0058 | 0,9304 ± 0,0204 | 0,0598 |
| RF | 1,0000 ± 0,0000 | 0,9564 ± 0,0232 | 0,0436 |

La poda baja la brecha de 7,3 a 6,0 puntos. No llega a los 9 y 3 puntos de la referencia de la tarjeta. El bosque queda en 4,4, más chico que las dos variantes del árbol. Los del árbol coinciden con la Tabla 5.

## Qué hacemos

La brecha es `media(accuracy train) − media(accuracy test)` sobre las 25 particiones del `cv` de la celda 1.1. `return_train_score=True` ya está en ese protocolo.

Tres barras agrupadas, train y test, con el desvío de las 25 particiones:

1. `DecisionTreeC45(pruning=False, random_state=SEED)`
2. `DecisionTreeC45(pruning=True, pruning_confidence=0.25, random_state=SEED)`
3. `RandomForestWrap` con 100 árboles, `max_features="sqrt"` y `random_state=SEED`

El bosque no tiene poda pesimista. Entra una sola vez, al lado de las dos variantes del árbol, para ver si su brecha queda más chica.

La figura sale en `figuras/fig7_brecha_train_test.png`. Los números van al informe. La tarjeta espera cerca de 9 puntos sin poda y cerca de 3 con poda. Si en este dataset no da eso, se publican los valores medidos.
